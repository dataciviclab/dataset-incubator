-- Mart IT NUTS3: Italian provinces, demographic profile
-- Note: median_age and over65_pct are NULL for Italy NUTS3
-- (Eurostat publishes age structure only at NUTS2 for Italy)
SELECT
    geo, year, country_code, geo_label_en,
    nuts_parent_code, nuts_parent_label_en,
    population, pop_density_km2,
    median_age, old_age_dependency_pct, youth_pct, total_dependency_pct,
    over65_pct, over75_pct,
    natural_change, net_migration, total_change
FROM clean_input
WHERE country_code = 'IT' AND nuts_level = 'NUTS3'
  AND population IS NOT NULL
