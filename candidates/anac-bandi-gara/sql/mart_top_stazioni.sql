-- ANAC: Top stazioni appaltanti per anno
-- Classifica delle amministrazioni che bandiscono di piu' (per importo e n. lotti),
-- con indicatore di frammentazione (lotti medi per gara).
SELECT
    anno_pubblicazione AS anno,
    cf_amministrazione_appaltante,
    denominazione_amministrazione_appaltante,
    sezione_regionale AS regione,
    COUNT(DISTINCT cig) AS n_gare,
    COUNT(*) AS n_lotti,
    ROUND(COUNT(*) * 1.0 / NULLIF(COUNT(DISTINCT cig), 0), 1) AS lotti_medi_per_gara,
    ROUND(SUM(importo_lotto), 0) AS importo_totale,
    ROUND(AVG(importo_lotto), 0) AS importo_medio,
    ROW_NUMBER() OVER (PARTITION BY anno_pubblicazione ORDER BY SUM(importo_lotto) DESC) AS rank_per_anno
FROM clean_input
WHERE stato = 'ATTIVO'
  AND cf_amministrazione_appaltante IS NOT NULL
  AND cf_amministrazione_appaltante != ''
GROUP BY anno, cf_amministrazione_appaltante, denominazione_amministrazione_appaltante, regione
ORDER BY anno DESC, rank_per_anno
LIMIT 500
