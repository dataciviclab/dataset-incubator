-- Mart trend: bandi pubblicati per anno (archivio completo OPEN+CLOSED)
-- Risponde a: quanti concorsi vengono banditi ogni anno? Il reclutamento PA è in crescita?
SELECT
    EXTRACT(YEAR FROM data_pubblicazione) AS anno,
    COUNT(*)                             AS num_bandi,
    SUM(num_posti)                       AS posti_totali,
    COUNT(DISTINCT ente)                 AS enti_distinti
FROM clean_input
WHERE data_pubblicazione IS NOT NULL
GROUP BY 1
ORDER BY 1
