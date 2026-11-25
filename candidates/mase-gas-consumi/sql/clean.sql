-- MASE SISEN — gas naturale distribuito per provincia × settore.
-- Input: raw_input.csv prodotto da preprocess.py, forma wide:
--   anno, regione, provincia, industriale, termoelettrico, reti
-- Il preprocess ha già risolto la regione (nella fonte è in fondo al blocco, sulla
-- riga "TOTALE" di regione) e scartato la colonna spacer e i totali.
-- Unità: M Sm3 (milioni di Sm3).

WITH src AS (
    SELECT
        TRY_CAST(NULLIF(TRIM(anno), '') AS INTEGER) AS anno,
        normalize_string(regione) AS regione,
        normalize_string(provincia) AS provincia,
        TRY_CAST(NULLIF(TRIM(industriale), '') AS DOUBLE) AS industriale,
        TRY_CAST(NULLIF(TRIM(termoelettrico), '') AS DOUBLE) AS termoelettrico,
        TRY_CAST(NULLIF(TRIM(reti), '') AS DOUBLE) AS reti
    FROM raw_input
    WHERE normalize_string(provincia) IS NOT NULL
),
long AS (
    UNPIVOT src
    ON industriale, termoelettrico, reti
    INTO NAME settore VALUE consumo_msmc
)
SELECT
    anno,
    regione,
    provincia,
    settore,
    consumo_msmc
FROM long
WHERE consumo_msmc IS NOT NULL
