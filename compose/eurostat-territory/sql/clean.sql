-- Clean: territory — area, tourism, crime, road accidents by NUTS3
-- Each row = (geo, year) with territorial indicators
-- Reads clean parquet from GCS via HTTPS (compose pattern)

WITH

-- ── Hub: all (geo × year) combinations EU-wide ────────────────────
hub AS (
    SELECT
        g.geo, g.geo_label_en, g.nuts_level,
        g.nuts_parent_code, g.nuts_parent_label_en,
        SUBSTRING(g.geo, 1, 2) AS country_code,
        a.year
    FROM (
        SELECT DISTINCT geo, geo_label_en, nuts_level,
            nuts_parent_code, nuts_parent_label_en
        FROM read_parquet(
            'https://storage.googleapis.com/dataciviclab-clean/eurostat/eurostat_area_nuts3/eurostat_area_nuts3_2026_clean.parquet',
            union_by_name=true
        )
        WHERE unit = 'KM2' AND landuse = 'TOTAL' AND year = 2024
            AND nuts_level IS NOT NULL
    ) g
    JOIN (
        SELECT DISTINCT year FROM read_parquet(
            'https://storage.googleapis.com/dataciviclab-clean/eurostat/eurostat_gdp_nuts3/eurostat_gdp_nuts3_2026_clean.parquet',
            union_by_name=true
        )
        WHERE unit = 'EUR_HAB'
    ) a ON (1=1)
),

-- 1. Land area (km²)
land_area AS (
    SELECT geo, year,
        AVG(value) AS area_km2
    FROM read_parquet(
        'https://storage.googleapis.com/dataciviclab-clean/eurostat/eurostat_area_nuts3/eurostat_area_nuts3_2026_clean.parquet',
        union_by_name=true
    )
    WHERE unit = 'KM2' AND landuse = 'TOTAL'
    GROUP BY geo, year
),

-- 2. Tourism: total nights spent
tourism AS (
    SELECT geo, year,
        SUM(value) AS total_nights_spent
    FROM read_parquet(
        'https://storage.googleapis.com/dataciviclab-clean/eurostat/eurostat_tourism_nuts3/eurostat_tourism_nuts3_2026_clean.parquet',
        union_by_name=true
    )
    WHERE c_resid = 'TOTAL' AND nace_r2 = 'I551-I553' AND unit = 'NR'
    GROUP BY geo, year
),

-- 3. Crime: total recorded offences
crime AS (
    SELECT geo, year,
        SUM(value) AS total_crimes
    FROM read_parquet(
        'https://storage.googleapis.com/dataciviclab-clean/eurostat/eurostat_crime_nuts3/eurostat_crime_nuts3_2026_clean.parquet',
        union_by_name=true
    )
    WHERE unit = 'NR'
    GROUP BY geo, year
),

-- 4. Road accidents
accidents AS (
    SELECT geo, year,
        SUM(value) AS road_accidents
    FROM read_parquet(
        'https://storage.googleapis.com/dataciviclab-clean/eurostat/eurostat_tran_sf_roadnu/eurostat_tran_sf_roadnu_2026_clean.parquet',
        union_by_name=true
    )
    WHERE unit = 'NR'
    GROUP BY geo, year
)

-- ── Final SELECT ───────────────────────────────────────────────────
SELECT
    -- 🔑 Key
    h.geo, h.year, h.nuts_level, h.country_code,
    h.geo_label_en, h.nuts_parent_code, h.nuts_parent_label_en,

    -- 📍 Land area
    la.area_km2,

    -- 🏨 Tourism
    t.total_nights_spent,

    -- 🚓 Crime
    cr.total_crimes,

    -- 🚗 Road accidents
    a.road_accidents

FROM hub h
LEFT JOIN land_area la ON h.geo = la.geo AND h.year = la.year
LEFT JOIN tourism t ON h.geo = t.geo AND h.year = t.year
LEFT JOIN crime cr ON h.geo = cr.geo AND h.year = cr.year
LEFT JOIN accidents a ON h.geo = a.geo AND h.year = a.year
-- Keep only rows with at least one real data point
WHERE la.area_km2 IS NOT NULL
   OR t.total_nights_spent IS NOT NULL
   OR cr.total_crimes IS NOT NULL
   OR a.road_accidents IS NOT NULL
ORDER BY h.country_code, h.nuts_level, h.geo, h.year
