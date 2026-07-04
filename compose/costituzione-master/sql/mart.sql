-- MART: costituzione-master
-- Vista analitica: metriche per articolo della Costituzione.

SELECT
    articolo,
    parte,
    heading,
    testo_preview,
    n_modifiche,
    n_giudizi,
    n_accolte,
    n_respinte,
    n_inammissibili,
    n_citazioni_legislative,
    n_indicatori,
    dataset_slugs,
    -- Classificazione
    CASE
        WHEN n_modifiche = 0 AND n_giudizi = 0
             AND n_citazioni_legislative = 0
             AND n_accolte = 0 AND n_respinte = 0 AND n_inammissibili = 0
        THEN 'mai toccato'
        WHEN n_modifiche > 0 AND n_giudizi > 0 THEN 'riformato e conteso'
        WHEN n_modifiche > 0 THEN 'riformato senza contenzioso'
        WHEN n_giudizi > 0 THEN 'principio conteso'
        ELSE 'solo citato o evocato'
    END AS profilo
FROM clean_input
