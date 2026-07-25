-- ANAC: Trend PNRR per anno, regione e settore
-- Confronto bandi PNRR vs non-PNRR: importi, n. lotti, n. stazioni appaltanti,
-- quota PNRR sul totale annuale per regione.
SELECT
    anno_pubblicazione,
    sezione_regionale,
    oggetto_principale_contratto,
    flag_pnrr,
    COUNT(*) AS n_lotti,
    COUNT(DISTINCT cig) AS n_bandi,
    COUNT(DISTINCT cf_amministrazione_appaltante) AS n_stazioni,
    ROUND(SUM(importo_lotto), 0) AS importo_totale,
    ROUND(AVG(importo_lotto), 0) AS importo_medio,
    -- quota PNRR sul totale del settore-regione-anno
    ROUND(SUM(importo_lotto) * 100.0
        / NULLIF(SUM(SUM(importo_lotto)) OVER (PARTITION BY anno_pubblicazione, sezione_regionale, oggetto_principale_contratto), 0), 2)
        AS quota_pct_settore
FROM clean_input
WHERE stato = 'ATTIVO'
  AND sezione_regionale IS NOT NULL
GROUP BY anno_pubblicazione, sezione_regionale, oggetto_principale_contratto, flag_pnrr
ORDER BY anno_pubblicazione DESC, sezione_regionale, oggetto_principale_contratto, flag_pnrr
