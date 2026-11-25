-- INAIL malattie — MART: distribuzione grado di menomazione.
SELECT
    grado_menomazione_caso,
    COUNT(*) AS n_casi,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct_casi,
    ROUND(AVG(giorni_indennizzati), 0) AS media_giorni_indennizzati
FROM clean_input
WHERE grado_menomazione_caso IS NOT NULL
GROUP BY grado_menomazione_caso
ORDER BY grado_menomazione_caso
