-- clean.sql: proiezioni demografiche ISTAT base 2025 → 2080
-- Canale: ZIP demo.istat.it (età×sesso) + RPCCerca.php (componenti bilancio)
-- Macros toolkit: normalize_string / cast_int / cast_double
--
-- Raw: grano, territorio_codice, componente_codice, anno, sesso, eta, valore
-- grano: eta_sesso | componenti

SELECT
    normalize_string(grano) AS grano,
    normalize_string(territorio_codice) AS territorio_codice,
    normalize_string(componente_codice) AS componente_codice,
    cast_int(anno) AS anno,
    normalize_string(sesso) AS sesso,
    normalize_string(eta) AS eta,
    cast_double(valore) AS valore
FROM raw_input
WHERE cast_int(anno) IS NOT NULL
  AND normalize_string(territorio_codice) IS NOT NULL
  AND normalize_string(grano) IS NOT NULL
  AND cast_double(valore) IS NOT NULL
