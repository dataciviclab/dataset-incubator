SELECT
    CAST(data_elezione AS DATE) AS data_elezione,
    CAST(regione AS VARCHAR) AS regione,
    CAST(provincia AS VARCHAR) AS provincia,
    CAST(comune AS VARCHAR) AS comune,
    TRY_CAST(turno AS BIGINT) AS turno,
    CAST(candidato AS VARCHAR) AS candidato,
    CAST(lista AS VARCHAR) AS lista,
    TRY_CAST(voti_candidato AS BIGINT) AS voti_candidato,
    TRY_CAST(voti_lista AS BIGINT) AS voti_lista,
    TRY_CAST(seggi_lista AS BIGINT) AS seggi_lista,
    TRY_CAST(elettori AS BIGINT) AS elettori,
    TRY_CAST(elettori_maschi AS BIGINT) AS elettori_maschi,
    TRY_CAST(votanti AS BIGINT) AS votanti,
    TRY_CAST(votanti_maschi AS BIGINT) AS votanti_maschi,
    TRY_CAST(schede_bianche AS BIGINT) AS schede_bianche
FROM raw_input
