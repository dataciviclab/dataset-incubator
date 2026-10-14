-- clean.sql: proiezioni demografiche ISTAT base 2025 → 2080
-- Canale: demo.istat.it RPCCerca.php (script preprocess → raw_input.csv)
-- Macros toolkit: normalize_string / cast_int / cast_double
--
-- Raw: territorio_codice, territorio, componente_codice, componente, anno, valore
-- Scenario mediano (median) da RPCCerca.php.

SELECT
    normalize_string(territorio_codice) AS territorio_codice,
    normalize_string(territorio) AS territorio,
    normalize_string(componente_codice) AS componente_codice,
    normalize_string(componente) AS componente,
    cast_int(anno) AS anno,
    cast_double(valore) AS valore
FROM raw_input
WHERE cast_int(anno) IS NOT NULL
  AND normalize_string(territorio_codice) IS NOT NULL
  AND normalize_string(componente_codice) IS NOT NULL
  AND cast_double(valore) IS NOT NULL
