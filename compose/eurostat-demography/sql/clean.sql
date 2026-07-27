-- Clean: demography — population, density, age structure, demographic balance
-- Each row = (geo, year) with demographic indicators
-- Reads clean parquet from GCS via HTTPS (compose pattern)

WITH

-- ── Geo anchor: area_nuts3, anno piu' recente disponibile ────────
area_data AS (
    SELECT * FROM read_parquet(
        'https://storage.googleapis.com/dataciviclab-clean/eurostat/eurostat_area_nuts3/eurostat_area_nuts3_2026_clean.parquet',
        union_by_name=true
    )
    WHERE unit = 'KM2' AND landuse = 'TOTAL'
),
geo_anchor AS (
    SELECT DISTINCT geo, geo_label_en, nuts_level,
        nuts_parent_code, nuts_parent_label_en
    FROM area_data
    WHERE year = (SELECT MAX(year) FROM area_data)
        AND nuts_level IS NOT NULL
),

-- ── Years: da demo_r_pjangrp3 (copertura 2014-2025) ─────────────
years AS (
    SELECT DISTINCT year FROM read_parquet(
        'https://storage.googleapis.com/dataciviclab-clean/eurostat/eurostat_demo_r_pjangrp3_nuts3/eurostat_demo_r_pjangrp3_nuts3_2026_clean.parquet',
        union_by_name=true
    )
    WHERE unit = 'NR' AND sex = 'T' AND age = 'TOTAL'
),

-- ── Hub: all (geo × year) combinations EU-wide ──────────────────
hub AS (
    SELECT
        g.geo, g.geo_label_en, g.nuts_level,
        g.nuts_parent_code, g.nuts_parent_label_en,
        SUBSTRING(g.geo, 1, 2) AS country_code,
        y.year
    FROM geo_anchor g
    CROSS JOIN years y
),

-- 1. Total population (from demo_r_pjangrp3 for NUTS3 coverage)
population AS (
    SELECT geo, year,
        SUM(value) AS population
    FROM read_parquet(
        'https://storage.googleapis.com/dataciviclab-clean/eurostat/eurostat_demo_r_pjangrp3_nuts3/eurostat_demo_r_pjangrp3_nuts3_2026_clean.parquet',
        union_by_name=true
    )
    WHERE unit = 'NR' AND sex = 'T' AND age = 'TOTAL'
    GROUP BY geo, year
),

-- 2. Population density
density AS (
    SELECT geo, year,
        AVG(value) AS pop_density_km2
    FROM read_parquet(
        'https://storage.googleapis.com/dataciviclab-clean/eurostat/eurostat_pop_density_nuts3/eurostat_pop_density_nuts3_2026_clean.parquet',
        union_by_name=true
    )
    WHERE unit = 'PER_KM2'
    GROUP BY geo, year
),

-- 3. Population structure indicators (age)
age_structure AS (
    SELECT geo, year,
        MAX(CASE WHEN indic_de = 'MEDAGEPOP' THEN value END) AS median_age,
        MAX(CASE WHEN indic_de = 'OLDDEP1' THEN value END) AS old_age_dependency_pct,
        MAX(CASE WHEN indic_de = 'PC_Y0_14' THEN value END) AS youth_pct,
        MAX(CASE WHEN indic_de = 'DEPRATIO1' THEN value END) AS total_dependency_pct,
        MAX(CASE WHEN indic_de = 'PC_Y65' THEN value END) AS over65_pct,
        MAX(CASE WHEN indic_de = 'PC_Y75' THEN value END) AS over75_pct
    FROM read_parquet(
        'https://storage.googleapis.com/dataciviclab-clean/eurostat/eurostat_pop_structure_nuts3/eurostat_pop_structure_nuts3_2026_clean.parquet',
        union_by_name=true
    )
    WHERE unit = 'PC' AND indic_de IN ('MEDAGEPOP', 'OLDDEP1', 'PC_Y0_14', 'DEPRATIO1', 'PC_Y65', 'PC_Y75')
    GROUP BY geo, year
),

-- 4. Demographic balance: natural change, net migration (per 1000 pop)
demographic_balance AS (
    SELECT geo, year,
        MAX(CASE WHEN indic_de = 'NATGROWRT' THEN value END) AS natural_change,
        MAX(CASE WHEN indic_de = 'CNMIGRATRT' THEN value END) AS net_migration,
        MAX(CASE WHEN indic_de = 'GROWRT' THEN value END) AS total_change
    FROM read_parquet(
        'https://storage.googleapis.com/dataciviclab-clean/eurostat/eurostat_demo_balance_nuts3/eurostat_demo_balance_nuts3_2026_clean.parquet',
        union_by_name=true
    )
    WHERE indic_de IN ('NATGROWRT', 'CNMIGRATRT', 'GROWRT')
    GROUP BY geo, year
)

-- ── Final SELECT ───────────────────────────────────────────────────
SELECT
    -- 🔑 Key
    h.geo, h.year, h.nuts_level, h.country_code,
    h.geo_label_en, h.nuts_parent_code, h.nuts_parent_label_en,

    -- 👥 Population
    pop.population,
    d.pop_density_km2,

    -- 📊 Age structure
    as_.median_age,
    as_.old_age_dependency_pct, as_.youth_pct, as_.total_dependency_pct,
    as_.over65_pct, as_.over75_pct,

    -- 🔄 Demographic balance
    db.natural_change, db.net_migration, db.total_change

FROM hub h
LEFT JOIN population pop ON h.geo = pop.geo AND h.year = pop.year
LEFT JOIN density d ON h.geo = d.geo AND h.year = d.year
LEFT JOIN age_structure as_ ON h.geo = as_.geo AND h.year = as_.year
LEFT JOIN demographic_balance db ON h.geo = db.geo AND h.year = db.year
-- Keep only rows with at least one real data point
WHERE pop.population IS NOT NULL
   OR d.pop_density_km2 IS NOT NULL
   OR as_.median_age IS NOT NULL
   OR db.natural_change IS NOT NULL
ORDER BY h.country_code, h.nuts_level, h.geo, h.year
