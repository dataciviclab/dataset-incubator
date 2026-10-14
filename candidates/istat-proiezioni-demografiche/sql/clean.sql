-- clean.sql: proiezioni demografiche ISTAT base 2025 → 2080
-- Fonte: ZIP demo.istat.it (età × sesso × regione, scenario mediano)
-- Macros toolkit: normalize_string / cast_int / cast_double

SELECT
    normalize_string(territorio_codice) AS territorio_codice,
    cast_int(anno) AS anno,
    normalize_string(sesso) AS sesso,
    normalize_string(eta) AS eta,
    cast_double(popolazione) AS popolazione
FROM raw_input
WHERE cast_int(anno) IS NOT NULL
  AND normalize_string(territorio_codice) IS NOT NULL
  AND normalize_string(sesso) IS NOT NULL
  AND normalize_string(eta) IS NOT NULL
  AND cast_double(popolazione) IS NOT NULL
