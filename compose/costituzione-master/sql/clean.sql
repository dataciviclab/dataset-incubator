-- CLEAN: costituzione-master
-- Già pulito da preprocess.py, solo cast e normalizzazione.

SELECT
    CAST(articolo AS INTEGER) AS articolo,
    TRIM(parte) AS parte,
    TRIM(heading) AS heading,
    TRIM(testo_preview) AS testo_preview,
    CAST(n_modifiche AS INTEGER) AS n_modifiche,
    CAST(n_giudizi AS INTEGER) AS n_giudizi,
    CAST(n_accolte AS INTEGER) AS n_accolte,
    CAST(n_respinte AS INTEGER) AS n_respinte,
    CAST(n_inammissibili AS INTEGER) AS n_inammissibili,
    CAST(n_citazioni_legislative AS INTEGER) AS n_citazioni_legislative,
    CAST(n_indicatori AS INTEGER) AS n_indicatori,
    TRIM(dataset_slugs) AS dataset_slugs
FROM raw_input
