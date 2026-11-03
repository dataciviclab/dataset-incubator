-- Consumo di gas distribuito per regione × settore, aggregato dalle province.
-- Il totale regionale è ricalcolato (non letto dalle righe "TOTALE" del foglio,
-- che il clean esclude) — serve da controllo di coerenza con la fonte.

SELECT
    anno,
    regione,
    settore,
    SUM(consumo_msmc) AS consumo_msmc,
    CASE
        WHEN SUM(SUM(consumo_msmc)) OVER (PARTITION BY anno, regione) > 0
        THEN 100.0 * SUM(consumo_msmc) / SUM(SUM(consumo_msmc)) OVER (PARTITION BY anno, regione)
        ELSE NULL
    END AS quota_regione_pct
FROM clean_input
GROUP BY anno, regione, settore
