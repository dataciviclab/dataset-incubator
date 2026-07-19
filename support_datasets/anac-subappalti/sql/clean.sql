SELECT
    cig,
    id_subappalto,
    cf_subappaltante,
    TRY_CAST(data_autorizzazione AS DATE) AS data_autorizzazione,
    oggetto,
    cod_categoria,
    descrizione_categoria,
    classe_importo,
    descrizione_tipo_categoria,
    cod_cpv,
    descrizione_cpv,
    codice_fiscale,
    denominazione,
    ruolo,
    tipo_soggetto
FROM raw_input
