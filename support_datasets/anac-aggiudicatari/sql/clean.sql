SELECT
    cig,
    ruolo,
    codice_fiscale,
    denominazione,
    tipo_soggetto,
    TRY_CAST(id_aggiudicazione AS BIGINT) AS id_aggiudicazione
FROM raw_input
