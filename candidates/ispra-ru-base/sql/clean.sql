-- ISPRA Rifiuti Urbani — CLEAN
-- Macro toolkit: cast_int, cast_bigint, cast_double, normalize_string, remove_dot_thousands
SELECT
    {year}::INTEGER AS anno,
    normalize_string(replace("IstatComune", chr(9), '')) AS codice_comune_istat,
    normalize_string("Regione") AS regione,
    normalize_string("Provincia") AS provincia,
    normalize_string("Comune") AS comune,
    cast_bigint(remove_dot_thousands("Popolazione")) AS popolazione,
    normalize_string("Dato riferito a") AS dato_riferito_a,
    normalize_italian_number("Totale RU (t)") AS totale_ru_tonnellate,
    normalize_italian_number("Totale RD (t)") AS totale_rd_tonnellate,
    -- Il campo ISPRA contiene "  64,79%" (con spazi e % finale)
    normalize_italian_number(replace("Percentuale RD (%)", '%', '')) AS percentuale_rd
FROM raw_input
WHERE normalize_string(replace("IstatComune", chr(9), '')) IS NOT NULL
  AND normalize_string("Dato riferito a") = 'Comune'
  AND cast_bigint(remove_dot_thousands("Popolazione")) IS NOT NULL
