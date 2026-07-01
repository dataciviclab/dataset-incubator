SELECT
    CAST(data_elezione AS DATE) AS data_elezione,
    CAST(regione AS VARCHAR) AS regione,
    CAST(circoscrizione AS VARCHAR) AS circoscrizione,
    CAST(provincia AS VARCHAR) AS provincia,
    CAST(comune AS VARCHAR) AS comune,
    TRY_CAST(elettori AS BIGINT) AS elettori,
    TRY_CAST(votanti AS BIGINT) AS votanti,
    TRY_CAST(schede_bianche AS BIGINT) AS schede_bianche,
    CAST(candidato AS VARCHAR) AS candidato,
    TRY_CAST(voti_candidato AS BIGINT) AS voti_candidato,
    CAST(lista AS VARCHAR) AS lista,
    TRY_CAST(voti_lista AS BIGINT) AS voti_lista
FROM raw_input
