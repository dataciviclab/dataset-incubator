-- mart.sql — ispra_consumo_suolo
-- mart_comuni: un record per comune × periodo, formato long con serie annuale
--
-- Le colonne stock_ha / stock_pct sono ricostruite in clean.sql.
-- Qui si applicano solo arrotondamenti e filtri finali.

SELECT
    pro_com,
    comune,
    provincia,
    regione,
    periodo,
    anno,
    incremento_netto_ha,
    incremento_lordo_ha,
    ripristino_ha,
    stock_ha,
    stock_pct

FROM clean_input

WHERE
    pro_com IS NOT NULL
    AND stock_ha IS NOT NULL
