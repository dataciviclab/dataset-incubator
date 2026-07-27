-- Mart IT NUTS3: Italian provinces, territorial profile
SELECT
    geo, year, country_code, geo_label_en,
    nuts_parent_code, nuts_parent_label_en,
    area_km2,
    total_nights_spent,
    total_crimes,
    road_accidents
FROM clean_input
WHERE country_code = 'IT' AND nuts_level = 'NUTS3'
  AND (total_nights_spent IS NOT NULL OR total_crimes IS NOT NULL OR road_accidents IS NOT NULL)
