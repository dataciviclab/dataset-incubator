-- Clean: economy — GDP, GVA, employment, labour productivity by NUTS3
-- Each row = (geo, year) with economic indicators
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

-- 1. GDP: per capita, total, PPS
gdp AS (
    SELECT geo, year,
        MAX(CASE WHEN unit = 'EUR_HAB' THEN value END) AS gdp_per_capita,
        MAX(CASE WHEN unit = 'MIO_EUR' THEN value END) AS gdp_million_eur,
        MAX(CASE WHEN unit = 'PPS_EU27_2020_HAB' THEN value END) AS gdp_pps_hab
    FROM read_parquet(
        'https://storage.googleapis.com/dataciviclab-clean/eurostat/eurostat_gdp_nuts3/eurostat_gdp_nuts3_2026_clean.parquet',
        union_by_name=true
    )
    WHERE unit IN ('EUR_HAB', 'MIO_EUR', 'PPS_EU27_2020_HAB')
    GROUP BY geo, year
),

-- 2. GVA: Gross Value Added by sector (current prices, million EUR)
gva AS (
    SELECT geo, year,
        SUM(CASE WHEN nace_r2 = 'TOTAL' THEN value END) AS gva_total_million,
        SUM(CASE WHEN nace_r2 = 'B-E' THEN value END) AS gva_industry_million,
        SUM(CASE WHEN nace_r2 = 'F' THEN value END) AS gva_construction_million,
        SUM(CASE WHEN nace_r2 = 'G-I' THEN value END) AS gva_trade_million,
        SUM(CASE WHEN nace_r2 = 'J' THEN value END) AS gva_ict_million,
        SUM(CASE WHEN nace_r2 = 'K-N' THEN value END) AS gva_financial_services_million,
        SUM(CASE WHEN nace_r2 = 'O-U' THEN value END) AS gva_public_admin_million
    FROM read_parquet(
        'https://storage.googleapis.com/dataciviclab-clean/eurostat/eurostat_gva_nuts3/eurostat_gva_nuts3_2026_clean.parquet',
        union_by_name=true
    )
    WHERE unit = 'CP_MEUR' AND nace_r2 IN ('TOTAL', 'B-E', 'F', 'G-I', 'J', 'K-N', 'O-U')
    GROUP BY geo, year
),

-- 3. Employment: total employed (thousands)
emp AS (
    SELECT geo, year,
        SUM(value) AS employment_thousands
    FROM read_parquet(
        'https://storage.googleapis.com/dataciviclab-clean/eurostat/eurostat_emp_nuts3/eurostat_emp_nuts3_2026_clean.parquet',
        union_by_name=true
    )
    WHERE unit = 'THS' AND wstatus = 'EMP' AND nace_r2 = 'TOTAL'
    GROUP BY geo, year
),

-- 4. Labour productivity: nominal per employed (EUR)
productivity AS (
    SELECT geo, year,
        AVG(value) AS nominal_labour_productivity_eur
    FROM read_parquet(
        'https://storage.googleapis.com/dataciviclab-clean/eurostat/eurostat_labour_productivity_nuts3/eurostat_labour_productivity_nuts3_2026_clean.parquet',
        union_by_name=true
    )
    WHERE na_item = 'NLPR_PER' AND unit = 'EUR'
    GROUP BY geo, year
)

-- ── Final SELECT ───────────────────────────────────────────────────
SELECT
    -- 🔑 Key
    h.geo, h.year, h.nuts_level, h.country_code,
    h.geo_label_en, h.nuts_parent_code, h.nuts_parent_label_en,

    -- 💼 GDP
    g.gdp_per_capita, g.gdp_million_eur, g.gdp_pps_hab,

    -- 🏭 GVA by sector
    va.gva_total_million,
    va.gva_industry_million, va.gva_construction_million, va.gva_trade_million,
    va.gva_ict_million, va.gva_financial_services_million, va.gva_public_admin_million,
    ROUND(va.gva_industry_million / NULLIF(va.gva_total_million, 0) * 100, 1) AS gva_industry_pct,
    ROUND(va.gva_construction_million / NULLIF(va.gva_total_million, 0) * 100, 1) AS gva_construction_pct,
    ROUND(va.gva_trade_million / NULLIF(va.gva_total_million, 0) * 100, 1) AS gva_trade_pct,
    ROUND(va.gva_ict_million / NULLIF(va.gva_total_million, 0) * 100, 1) AS gva_ict_pct,
    ROUND(va.gva_financial_services_million / NULLIF(va.gva_total_million, 0) * 100, 1) AS gva_financial_services_pct,
    ROUND(va.gva_public_admin_million / NULLIF(va.gva_total_million, 0) * 100, 1) AS gva_public_admin_pct,

    -- 👷 Employment & productivity
    e.employment_thousands,
    p.nominal_labour_productivity_eur,
    -- GDP per employed (efficiency proxy)
    ROUND(g.gdp_million_eur * 1000 / NULLIF(e.employment_thousands, 0), 0) AS gdp_per_employed_eur

FROM hub h
LEFT JOIN gdp g ON h.geo = g.geo AND h.year = g.year
LEFT JOIN gva va ON h.geo = va.geo AND h.year = va.year
LEFT JOIN emp e ON h.geo = e.geo AND h.year = e.year
LEFT JOIN productivity p ON h.geo = p.geo AND h.year = p.year
-- Keep only rows with at least one real data point (no all-NULL rows)
WHERE g.gdp_per_capita IS NOT NULL
   OR g.gdp_million_eur IS NOT NULL
   OR va.gva_total_million IS NOT NULL
   OR e.employment_thousands IS NOT NULL
ORDER BY h.country_code, h.nuts_level, h.geo, h.year
