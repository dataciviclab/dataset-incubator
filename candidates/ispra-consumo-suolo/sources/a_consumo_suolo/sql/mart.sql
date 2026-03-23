-- mart.sql — ispra_consumo_suolo
-- mart_comuni: un record per comune, snapshot 2024 piu serie incrementi per periodo

SELECT
    clean.pro_com,
    clean.comune,
    clean.provincia,
    clean.regione,
    ROUND(clean.incremento_netto_ha_2006_2012, 4) AS incremento_netto_ha_2006_2012,
    ROUND(clean.incremento_lordo_ha_2006_2012, 4) AS incremento_lordo_ha_2006_2012,
    ROUND(clean.incremento_netto_ha_2012_2015, 4) AS incremento_netto_ha_2012_2015,
    ROUND(clean.incremento_lordo_ha_2012_2015, 4) AS incremento_lordo_ha_2012_2015,
    ROUND(clean.incremento_netto_ha_2015_2016, 4) AS incremento_netto_ha_2015_2016,
    ROUND(clean.incremento_lordo_ha_2015_2016, 4) AS incremento_lordo_ha_2015_2016,
    ROUND(clean.incremento_netto_ha_2016_2017, 4) AS incremento_netto_ha_2016_2017,
    ROUND(clean.incremento_lordo_ha_2016_2017, 4) AS incremento_lordo_ha_2016_2017,
    ROUND(clean.incremento_netto_ha_2017_2018, 4) AS incremento_netto_ha_2017_2018,
    ROUND(clean.incremento_lordo_ha_2017_2018, 4) AS incremento_lordo_ha_2017_2018,
    ROUND(clean.incremento_netto_ha_2018_2019, 4) AS incremento_netto_ha_2018_2019,
    ROUND(clean.incremento_lordo_ha_2018_2019, 4) AS incremento_lordo_ha_2018_2019,
    ROUND(clean.incremento_netto_ha_2019_2020, 4) AS incremento_netto_ha_2019_2020,
    ROUND(clean.incremento_lordo_ha_2019_2020, 4) AS incremento_lordo_ha_2019_2020,
    ROUND(clean.incremento_netto_ha_2020_2021, 4) AS incremento_netto_ha_2020_2021,
    ROUND(clean.incremento_lordo_ha_2020_2021, 4) AS incremento_lordo_ha_2020_2021,
    ROUND(clean.incremento_netto_ha_2021_2022, 4) AS incremento_netto_ha_2021_2022,
    ROUND(clean.incremento_lordo_ha_2021_2022, 4) AS incremento_lordo_ha_2021_2022,
    ROUND(clean.incremento_netto_ha_2022_2023, 4) AS incremento_netto_ha_2022_2023,
    ROUND(clean.incremento_lordo_ha_2022_2023, 4) AS incremento_lordo_ha_2022_2023,
    ROUND(clean.incremento_ha_2023_2024, 4) AS incremento_ha_2023_2024,
    ROUND(clean.incremento_netto_ha_2023_2024, 4) AS incremento_netto_ha_2023_2024,
    ROUND(clean.incremento_lordo_ha_2023_2024, 4) AS incremento_lordo_ha_2023_2024,
    ROUND(clean.stock_ha_2024, 2) AS stock_ha_2024,
    ROUND(clean.stock_pct_2024, 4) AS stock_pct_2024

FROM clean

WHERE
    pro_com IS NOT NULL
    AND stock_ha_2024 IS NOT NULL

ORDER BY stock_ha_2024 DESC
