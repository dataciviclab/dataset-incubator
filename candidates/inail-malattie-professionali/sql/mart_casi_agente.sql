-- INAIL malattie — MART: casi per agente causale × settore.
SELECT
    agente_causale,
    settore_correlato,
    COUNT(*) AS n_casi,
    ROUND(AVG(grado_menomazione_caso), 1) AS media_menomazione,
    ROUND(AVG(giorni_indennizzati), 0) AS media_giorni_indennizzati
FROM clean_input
WHERE agente_causale IS NOT NULL
  AND settore_correlato IS NOT NULL
GROUP BY agente_causale, settore_correlato
HAVING COUNT(*) >= 5
ORDER BY n_casi DESC
