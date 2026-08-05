SELECT
    codice_univoco_submisura,
    descrizione_submisura,
    COUNT(*) AS n_gare,
    COUNT(DISTINCT cig) AS n_cig,
    COUNT(DISTINCT cup) AS n_cup,
    ROUND(SUM(importo_complessivo_gara)) AS tot_importo_complessivo,
    ROUND(SUM(importo_aggiudicazione)) AS tot_importo_aggiudicazione,
    ROUND(AVG(importo_aggiudicazione)) AS media_importo_aggiudicazione,
    COUNT(*) FILTER (WHERE data_aggiudicazione_definitiva IS NOT NULL) AS n_aggiudicate
FROM clean_input
GROUP BY codice_univoco_submisura, descrizione_submisura
