SELECT
    CAST(data_elezione AS DATE) AS data_elezione,
    CAST(circoscrizione AS VARCHAR) AS circoscrizione,
    CAST(regione AS VARCHAR) AS regione,
    CAST(provincia AS VARCHAR) AS provincia,
    CAST(comune AS VARCHAR) AS comune,
    CAST(lista AS VARCHAR) AS lista,
    TRY_CAST(voti_lista AS BIGINT) AS voti_lista,
    TRY_CAST(elettori AS BIGINT) AS elettori,
    TRY_CAST(votanti AS BIGINT) AS votanti,
    TRY_CAST(schede_bianche AS BIGINT) AS schede_bianche
FROM raw_input
