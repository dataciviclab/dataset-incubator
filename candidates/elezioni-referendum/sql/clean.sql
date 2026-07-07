SELECT
    CAST(data_elezione AS DATE) AS data_elezione,
    CAST(regione AS VARCHAR) AS regione,
    CAST(provincia AS VARCHAR) AS provincia,
    CAST(comune AS VARCHAR) AS comune,
    TRY_CAST(elettori_uomini AS BIGINT) AS elettori_uomini,
    TRY_CAST(elettori AS BIGINT) AS elettori,
    TRY_CAST(votanti_uomini AS BIGINT) AS votanti_uomini,
    TRY_CAST(votanti AS BIGINT) AS votanti,
    TRY_CAST(voti_si AS BIGINT) AS voti_si,
    TRY_CAST(voti_no AS BIGINT) AS voti_no,
    TRY_CAST(schede_nulle AS BIGINT) AS schede_nulle,
    TRY_CAST(schede_bianche AS BIGINT) AS schede_bianche,
    TRY_CAST(schede_contestate AS BIGINT) AS schede_contestate,
    TRY_CAST(num_quesito AS BIGINT) AS num_quesito
FROM raw_input
