SELECT
    cig,
    TRY_CAST(data_aggiudicazione_definitiva AS DATE) AS data_aggiudicazione_definitiva,
    esito,
    criterio_aggiudicazione,
    TRY_CAST(data_comunicazione_esito AS DATE) AS data_comunicazione_esito,
    TRY_CAST(numero_offerte_ammesse AS INTEGER) AS numero_offerte_ammesse,
    TRY_CAST(numero_offerte_escluse AS INTEGER) AS numero_offerte_escluse,
    TRY_CAST(importo_aggiudicazione AS DOUBLE) AS importo_aggiudicazione,
    TRY_CAST(ribasso_aggiudicazione AS DOUBLE) AS ribasso_aggiudicazione,
    TRY_CAST(num_imprese_offerenti AS INTEGER) AS num_imprese_offerenti,
    CASE WHEN flag_subappalto::VARCHAR IN ('1', 'true', 'TRUE', 'S') THEN TRUE
         WHEN flag_subappalto::VARCHAR IN ('0', 'false', 'FALSE', 'N') THEN FALSE
         ELSE NULL END AS flag_subappalto,
    TRY_CAST(id_aggiudicazione AS BIGINT) AS id_aggiudicazione,
    TRY_CAST(cod_esito AS INTEGER) AS cod_esito,
    TRY_CAST(num_imprese_richiedenti AS INTEGER) AS num_imprese_richiedenti,
    CASE WHEN asta_elettronica::VARCHAR IN ('1', 'true', 'TRUE', 'S') THEN TRUE
         WHEN asta_elettronica::VARCHAR IN ('0', 'false', 'FALSE', 'N') THEN FALSE
         ELSE NULL END AS asta_elettronica,
    TRY_CAST(num_imprese_invitate AS INTEGER) AS num_imprese_invitate,
    TRY_CAST(massimo_ribasso AS DOUBLE) AS massimo_ribasso,
    TRY_CAST(minimo_ribasso AS DOUBLE) AS minimo_ribasso,
    -- raw columns pass-through (nullable, schema variabile)
    FLAG_SCOMPUTO,
    TRY_CAST(COD_PRESTAZIONI_COMPRESE AS DOUBLE) AS COD_PRESTAZIONI_COMPRESE,
    PRESTAZIONI_COMPRESE,
    CIG_PROG_ESTERNA,
    TRY_CAST(DATA_INCARICO_PROG AS DATE) AS DATA_INCARICO_PROG,
    TRY_CAST(DATA_CONS_PROG AS DATE) AS DATA_CONS_PROG,
    TRY_CAST(COD_MODO_RIAGGIUDICAZIONE AS DOUBLE) AS COD_MODO_RIAGGIUDICAZIONE,
    MODO_RIAGGIUDICAZIONE,
    CASE WHEN FLAG_PROC_ACCELERATA::VARCHAR IN ('1', 'true', 'TRUE', 'S') THEN TRUE
         WHEN FLAG_PROC_ACCELERATA::VARCHAR IN ('0', 'false', 'FALSE', 'N') THEN FALSE
         ELSE NULL END AS FLAG_PROC_ACCELERATA,
    TRY_CAST(N_MANIF_INTERESSE AS INTEGER) AS N_MANIF_INTERESSE
FROM raw_input
