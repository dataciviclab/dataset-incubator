-- Consumo di gas distribuito per provincia × settore, con quota sul totale provinciale.
-- Formato lungo (tidy): una riga per provincia × settore.

SELECT
    anno,
    regione,
    provincia,
    settore,
    consumo_msmc,
    CASE
        WHEN SUM(consumo_msmc) OVER (PARTITION BY anno, provincia) > 0
        THEN 100.0 * consumo_msmc / SUM(consumo_msmc) OVER (PARTITION BY anno, provincia)
        ELSE NULL
    END AS quota_provincia_pct
FROM clean_input
