SELECT
    TRY_CAST(Data AS DATE) AS data_sbarchi,
    TRY_CAST(Valore AS BIGINT) AS valore,
    CAST(Note AS VARCHAR) AS note,
    CAST(Fonte AS VARCHAR) AS fonte
FROM raw_input
WHERE TRY_CAST(Valore AS BIGINT) IS NOT NULL
