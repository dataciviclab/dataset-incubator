SELECT
    TRY_CAST(ANNO AS INTEGER) AS anno,
    CAST(settore AS VARCHAR) AS settore,
    normalize_string(REGIONE) AS regione,
    normalize_string("DIREZIONE REGIONALE") AS direzione_regionale,
    -- Normalizza 1.410 e 1410 -> 1410 (stesso capitolo di bilancio)
    TRY_CAST(replace("CODICE CAPITOLO", '.', '') AS BIGINT) AS codice_capitolo,
    TRY_CAST("CODICE ARTICOLO" AS BIGINT) AS codice_articolo,
    normalize_string("DESCRIZIONE TIPO TRIBUTO") AS descrizione_tributo,
    normalize_string("DESCRIZIONE ACCISE") AS descrizione_accisa,
    TRY_CAST(normalize_italian_number("ACCERTATO") AS DOUBLE) AS accertato
FROM raw_input
WHERE TRY_CAST(ANNO AS INTEGER) IS NOT NULL
  AND normalize_string(REGIONE) IS NOT NULL
  AND "ACCERTATO" IS NOT NULL
  AND TRIM("ACCERTATO") <> ''
