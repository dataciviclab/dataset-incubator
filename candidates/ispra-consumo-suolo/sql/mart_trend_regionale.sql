-- mart_trend_regionale.sql — ispra_consumo_suolo
-- Trend annuale per regione del consumo di suolo (solo periodi annuali 2016-2024)

SELECT
    regione,
    anno,
    COUNT(*)                                            AS comuni,
    ROUND(AVG(stock_pct), 3)                            AS avg_stock_pct,
    ROUND(SUM(stock_ha), 1)                             AS tot_stock_ha,
    ROUND(AVG(incremento_netto_ha), 2)                  AS avg_inc_netto_ha,
    ROUND(SUM(incremento_netto_ha), 1)                  AS tot_inc_netto_ha,
    ROUND(SUM(incremento_lordo_ha), 1)                  AS tot_inc_lordo_ha,
    ROUND(SUM(ripristino_ha), 1)                        AS tot_ripristino_ha

FROM clean_input

WHERE
    periodo NOT IN ('2006-2012', '2012-2015')
    AND stock_ha IS NOT NULL

GROUP BY regione, anno
ORDER BY regione, anno DESC
