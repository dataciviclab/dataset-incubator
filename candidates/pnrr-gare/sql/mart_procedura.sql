SELECT
    COALESCE(NULLIF(descrizione_procedura_aggiudicazione, ''), 'NON DICHIARATA') AS descrizione_procedura_aggiudicazione,
    COUNT(*) AS n_gare,
    COUNT(DISTINCT cig) AS n_cig,
    ROUND(SUM(importo_aggiudicazione)) AS tot_importo_aggiudicazione,
    ROUND(AVG(importo_aggiudicazione)) AS media_importo_aggiudicazione,
    COUNT(*) FILTER (WHERE data_aggiudicazione_definitiva IS NOT NULL) AS n_aggiudicate
FROM clean_input
GROUP BY 1
