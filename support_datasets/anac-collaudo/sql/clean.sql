-- Macro toolkit: cast_int, cast_double
SELECT
    normalize_string(cig) AS cig,
    TRY_CAST(data_delibera AS DATE) AS data_delibera,
    TRY_CAST(data_cert_collaudo AS DATE) AS data_cert_collaudo,
    normalize_string(esito_collaudo) AS esito_collaudo,
    TRY_CAST(data_inizio_oper AS DATE) AS data_inizio_oper,
    TRY_CAST(data_regolare_esec AS DATE) AS data_regolare_esec,
    TRY_CAST(data_nomina_coll AS DATE) AS data_nomina_coll,
    TRY_CAST(data_collaudo_stat AS DATE) AS data_collaudo_stat,
    cast_int(id_aggiudicazione) AS id_aggiudicazione,
    cast_double(RISERVE_AVANZATE) AS riserve_avanzate,
    cast_double(RISERVE_DEFINITE) AS riserve_definite,
    cast_double(IMPORTO_CONTENZ_RISOLTO) AS importo_contenz_risolto
FROM raw_input
WHERE cig IS NOT NULL AND TRIM(cig) != ''
