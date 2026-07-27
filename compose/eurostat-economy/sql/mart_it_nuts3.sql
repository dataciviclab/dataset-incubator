-- Mart IT NUTS3: Italian provinces, full economic profile
SELECT
    geo, year, country_code, geo_label_en,
    nuts_parent_code, nuts_parent_label_en,

    -- GDP
    gdp_per_capita, gdp_million_eur, gdp_pps_hab,

    -- GVA by sector
    gva_total_million,
    gva_industry_million, gva_construction_million, gva_trade_million,
    gva_ict_million, gva_financial_services_million, gva_public_admin_million,
    gva_industry_pct, gva_construction_pct, gva_trade_pct,
    gva_ict_pct, gva_financial_services_pct, gva_public_admin_pct,

    -- Employment
    employment_thousands, nominal_labour_productivity_eur,
    gdp_per_employed_eur

FROM clean_input
WHERE country_code = 'IT' AND nuts_level = 'NUTS3'
  -- Keep rows with at least one economic indicator
  AND (gdp_per_capita IS NOT NULL OR employment_thousands IS NOT NULL)
