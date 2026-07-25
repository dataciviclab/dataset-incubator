-- IRPEF: Disuguaglianza intra-regionale del reddito
-- Per ogni regione: differenza tra comune con reddito medio piu' alto
-- e piu' basso, deviazione standard, coefficiente di variazione.
-- Dove la disuguaglianza interna e' maggiore?
WITH comuni_reddito AS (
    SELECT
        anno_di_imposta AS anno,
        regione,
        denominazione_comune AS comune,
        sigla_provincia AS provincia,
        numero_contribuenti,
        ROUND(reddito_imponibile_eur / NULLIF(numero_contribuenti, 0), 0) AS reddito_medio,
        imposta_netta_eur / NULLIF(numero_contribuenti, 0) AS imposta_media
    FROM clean_input
    WHERE regione IS NOT NULL
      AND numero_contribuenti > 0
      AND reddito_imponibile_eur > 0
)
SELECT
    anno,
    regione,
    COUNT(*) AS comuni,
    ROUND(MIN(reddito_medio), 0) AS reddito_medio_min,
    ROUND(MAX(reddito_medio), 0) AS reddito_medio_max,
    ROUND(AVG(reddito_medio), 0) AS reddito_medio_regionale,
    ROUND(MAX(reddito_medio) - MIN(reddito_medio), 0) AS delta_max_min,
    ROUND(STDDEV_SAMP(reddito_medio), 0) AS devstd_reddito,
    -- Coefficiente di variazione (CV): devstd / media
    ROUND(STDDEV_SAMP(reddito_medio) * 100.0 / NULLIF(AVG(reddito_medio), 0), 2) AS cv_pct,
    -- Rapporto tra il 90° e il 10° percentile approssimato
    ROUND(MAX(reddito_medio) * 1.0 / NULLIF(MIN(reddito_medio), 1), 1) AS rapporto_max_min,
    -- Media pesata per popolazione (reddito medio regionale reale)
    ROUND(SUM(reddito_medio * numero_contribuenti) / NULLIF(SUM(numero_contribuenti), 0), 0) AS reddito_medio_ponderato
FROM comuni_reddito
GROUP BY anno, regione
ORDER BY anno DESC, cv_pct DESC
