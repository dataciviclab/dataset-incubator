-- mart.sql — ispra_consumo_suolo
-- mart_comuni: un record per comune, dati stock e incremento 2024

SELECT
    pro_com,
    comune,
    provincia,
    regione,
    ROUND(incremento_ha_2023_2024, 4) AS incremento_ha_2023_2024,
    ROUND(stock_ha_2024,           2) AS stock_ha_2024,
    ROUND(stock_pct_2024,          4) AS stock_pct_2024

FROM clean

WHERE
    pro_com IS NOT NULL
    AND stock_ha_2024 IS NOT NULL

ORDER BY stock_ha_2024 DESC
