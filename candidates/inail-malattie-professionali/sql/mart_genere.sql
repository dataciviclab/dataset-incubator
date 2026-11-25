-- INAIL malattie — MART: casi per genere con breakdown settore.
SELECT
    genere,
    COUNT(*) AS n_casi,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct_casi,
    ROUND(AVG(grado_menomazione_caso), 1) AS media_menomazione,
    ROUND(AVG(giorni_indennizzati), 0) AS media_giorni_indennizzati,
    COUNT(DISTINCT icd10_denunciato) AS n_patologie,
    COUNT(DISTINCT agente_causale) AS n_agenti
FROM clean_input
WHERE genere IS NOT NULL
GROUP BY genere
ORDER BY n_casi DESC
