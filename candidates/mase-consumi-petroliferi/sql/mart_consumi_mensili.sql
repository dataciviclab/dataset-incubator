-- Consumi petroliferi mensili per prodotto.
-- `quota_pct` è calcolata sui 7 prodotti reali, escludendo la riga di totale
-- (`totale prodotti principali`), che è una vista di sintesi e non una voce:
-- per quella riga la quota è NULL.

SELECT
    anno,
    mese,
    prodotto,
    consumo_kt,
    CASE
        WHEN prodotto = 'totale prodotti principali' THEN NULL
        WHEN SUM(consumo_kt) FILTER (WHERE prodotto <> 'totale prodotti principali')
                 OVER (PARTITION BY anno, mese) > 0
        THEN 100.0 * consumo_kt
             / SUM(consumo_kt) FILTER (WHERE prodotto <> 'totale prodotti principali')
                   OVER (PARTITION BY anno, mese)
        ELSE NULL
    END AS quota_pct
FROM clean_input
