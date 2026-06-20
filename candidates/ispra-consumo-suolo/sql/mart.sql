-- mart.sql — ispra_consumo_suolo
-- mart_comuni: un record per comune, snapshot 2024 piu serie incrementi per periodo

SELECT
    pro_com,
    comune,
    provincia,
    regione,
    ROUND(incremento_netto_ha_2006_2012, 4) AS incremento_netto_ha_2006_2012,
    ROUND(incremento_lordo_ha_2006_2012, 4) AS incremento_lordo_ha_2006_2012,
    ROUND(ripristino_ha_2006_2012, 4)       AS ripristino_ha_2006_2012,
    ROUND(incremento_netto_ha_2012_2015, 4) AS incremento_netto_ha_2012_2015,
    ROUND(incremento_lordo_ha_2012_2015, 4) AS incremento_lordo_ha_2012_2015,
    ROUND(ripristino_ha_2012_2015, 4)       AS ripristino_ha_2012_2015,
    ROUND(incremento_netto_ha_2015_2016, 4) AS incremento_netto_ha_2015_2016,
    ROUND(incremento_lordo_ha_2015_2016, 4) AS incremento_lordo_ha_2015_2016,
    ROUND(ripristino_ha_2015_2016, 4)       AS ripristino_ha_2015_2016,
    ROUND(incremento_netto_ha_2016_2017, 4) AS incremento_netto_ha_2016_2017,
    ROUND(incremento_lordo_ha_2016_2017, 4) AS incremento_lordo_ha_2016_2017,
    ROUND(ripristino_ha_2016_2017, 4)       AS ripristino_ha_2016_2017,
    ROUND(incremento_netto_ha_2017_2018, 4) AS incremento_netto_ha_2017_2018,
    ROUND(incremento_lordo_ha_2017_2018, 4) AS incremento_lordo_ha_2017_2018,
    ROUND(ripristino_ha_2017_2018, 4)       AS ripristino_ha_2017_2018,
    ROUND(incremento_netto_ha_2018_2019, 4) AS incremento_netto_ha_2018_2019,
    ROUND(incremento_lordo_ha_2018_2019, 4) AS incremento_lordo_ha_2018_2019,
    ROUND(ripristino_ha_2018_2019, 4)       AS ripristino_ha_2018_2019,
    ROUND(incremento_netto_ha_2019_2020, 4) AS incremento_netto_ha_2019_2020,
    ROUND(incremento_lordo_ha_2019_2020, 4) AS incremento_lordo_ha_2019_2020,
    ROUND(ripristino_ha_2019_2020, 4)       AS ripristino_ha_2019_2020,
    ROUND(incremento_netto_ha_2020_2021, 4) AS incremento_netto_ha_2020_2021,
    ROUND(incremento_lordo_ha_2020_2021, 4) AS incremento_lordo_ha_2020_2021,
    ROUND(ripristino_ha_2020_2021, 4)       AS ripristino_ha_2020_2021,
    ROUND(incremento_netto_ha_2021_2022, 4) AS incremento_netto_ha_2021_2022,
    ROUND(incremento_lordo_ha_2021_2022, 4) AS incremento_lordo_ha_2021_2022,
    ROUND(ripristino_ha_2021_2022, 4)       AS ripristino_ha_2021_2022,
    ROUND(incremento_netto_ha_2022_2023, 4) AS incremento_netto_ha_2022_2023,
    ROUND(incremento_lordo_ha_2022_2023, 4) AS incremento_lordo_ha_2022_2023,
    ROUND(ripristino_ha_2022_2023, 4)       AS ripristino_ha_2022_2023,
    ROUND(incremento_netto_ha_2023_2024, 4) AS incremento_netto_ha_2023_2024,
    ROUND(incremento_lordo_ha_2023_2024, 4) AS incremento_lordo_ha_2023_2024,
    ROUND(ripristino_ha_2023_2024, 4)       AS ripristino_ha_2023_2024,
    ROUND(stock_ha_2024, 2)                AS stock_ha_2024,
    ROUND(stock_pct_2024, 4)              AS stock_pct_2024

FROM clean_input

WHERE
    pro_com IS NOT NULL
    AND stock_ha_2024 IS NOT NULL
