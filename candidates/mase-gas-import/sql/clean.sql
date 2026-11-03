-- MASE SISEN — import di gas naturale per paese di origine.
-- Input: raw_input.csv prodotto da preprocess.py (serie già normalizzata).
--   anno, mese, paese_origine, import_msmc
--   `mese` vuoto = dato annuale (anni 1990-2001, non coperti dai file mensili).
-- Unità: M Sm3 (milioni di Sm3). Il preprocess ha già riscalato i file 2013-2014
-- (in Sm3 grezzi nonostante il titolo "Miliardi").

SELECT
    TRY_CAST(NULLIF(TRIM(anno), '') AS INTEGER) AS anno,
    TRY_CAST(NULLIF(TRIM(mese), '') AS INTEGER) AS mese,
    CASE WHEN NULLIF(TRIM(mese), '') IS NULL THEN 'annuale' ELSE 'mensile' END AS granularita,
    normalize_string(paese_origine) AS paese_origine,
    TRY_CAST(NULLIF(TRIM(import_msmc), '') AS DOUBLE) AS import_msmc
FROM raw_input
WHERE normalize_string(paese_origine) IS NOT NULL
  AND TRY_CAST(NULLIF(TRIM(import_msmc), '') AS DOUBLE) IS NOT NULL
