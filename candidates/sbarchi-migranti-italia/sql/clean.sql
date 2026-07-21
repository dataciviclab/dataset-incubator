SELECT
    TRY_CAST(Data AS DATE) AS data_sbarchi,
    cast_bigint(Valore) AS valore,
    normalize_string(Note) AS note,
    normalize_string(Fonte) AS fonte
FROM raw_input
WHERE cast_bigint(Valore) IS NOT NULL
