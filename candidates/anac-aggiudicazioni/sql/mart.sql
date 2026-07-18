SELECT
    year(data_aggiudicazione_definitiva) AS anno_aggiudicazione,
    month(data_aggiudicazione_definitiva) AS mese_aggiudicazione,
    esito,
    criterio_aggiudicazione,
    flag_subappalto,
    asta_elettronica,
    CASE WHEN importo_aggiudicazione > 0 THEN TRUE ELSE FALSE END AS flag_importo_positivo,
    COUNT(*) AS n_aggiudicazioni,
    COUNT(DISTINCT cig) AS n_cig_distinti,
    COUNT(DISTINCT id_aggiudicazione) AS n_id_aggiudicazione_distinti,
    SUM(importo_aggiudicazione) AS importo_totale,
    AVG(importo_aggiudicazione) AS importo_medio,
    MEDIAN(importo_aggiudicazione) AS importo_mediano,
    MAX(importo_aggiudicazione) AS importo_massimo,
    MIN(importo_aggiudicazione) AS importo_minimo,
    AVG(ribasso_aggiudicazione) AS ribasso_medio,
    MEDIAN(ribasso_aggiudicazione) AS ribasso_mediano,
    SUM(numero_offerte_ammesse) AS offerte_ammesse_totale,
    SUM(numero_offerte_escluse) AS offerte_escluse_totale,
    AVG(num_imprese_offerenti) AS imprese_offerenti_medie,
    AVG(num_imprese_invitate) AS imprese_invitate_medie
FROM clean_input
WHERE data_aggiudicazione_definitiva IS NOT NULL
  AND year(data_aggiudicazione_definitiva) BETWEEN 2005 AND 2026
GROUP BY
    year(data_aggiudicazione_definitiva),
    month(data_aggiudicazione_definitiva),
    esito,
    criterio_aggiudicazione,
    flag_subappalto,
    asta_elettronica,
    CASE WHEN importo_aggiudicazione > 0 THEN TRUE ELSE FALSE END
