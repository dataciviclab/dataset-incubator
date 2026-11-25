-- INAIL malattie — MART: casi per settore economico correlato.
SELECT
    settore_correlato,
    COUNT(*) AS n_casi,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct_casi,
    ROUND(AVG(grado_menomazione_caso), 1) AS media_menomazione,
    ROUND(AVG(giorni_indennizzati), 0) AS media_giorni_indennizzati
FROM clean_input
WHERE settore_correlato IS NOT NULL
GROUP BY settore_correlato
ORDER BY n_casi DESC
