-- Consumi petroliferi annuali per prodotto, con quota % sull'anno.
-- È la tabella per leggere il trend 2002-2025.

SELECT
    anno,
    prodotto,
    SUM(consumo_kt) AS consumo_kt,
    CASE
        WHEN prodotto = 'totale prodotti principali' THEN NULL
        WHEN SUM(SUM(consumo_kt)) FILTER (WHERE prodotto <> 'totale prodotti principali')
                 OVER (PARTITION BY anno) > 0
        THEN 100.0 * SUM(consumo_kt)
             / SUM(SUM(consumo_kt)) FILTER (WHERE prodotto <> 'totale prodotti principali')
                   OVER (PARTITION BY anno)
        ELSE NULL
    END AS quota_pct
FROM clean_input
GROUP BY anno, prodotto
