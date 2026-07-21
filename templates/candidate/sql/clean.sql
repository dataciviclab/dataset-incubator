-- clean.sql — template per nuovi dataset
--
-- Il toolkit carica automaticamente le macro DuckDB standard:
--   normalize_string(col)        TRIM + stringa vuota → NULL
--   cast_int(col)                TRY_CAST(... AS INTEGER)
--   cast_bigint(col)             TRY_CAST(... AS BIGINT)
--   cast_double(col)             TRY_CAST(... AS DOUBLE)
--   normalize_italian_number(c)  "1.234,56" → 1234.56
--   normalize_italian_integer(c) "1.234" → 1234 (arrotonda)
--   decode_flag(col, 'X')        flag testuale → BOOLEAN
--   remove_dot_thousands(col)    solo per interi con punti migliaia
--
-- Documentazione completa: https://github.com/dataciviclab/toolkit/blob/main/docs/standard-macros.md
--
-- Esempi (sostituisci con le tue colonne):
--
-- SELECT
--     {year}::INTEGER AS anno,
--     cast_int("Codice") AS codice,
--     normalize_string("Nome") AS nome,
--     cast_double("Valore") AS valore,
--     normalize_italian_number("Importo") AS importo,
--     decode_flag("Flag", 'X') AS flag_attivo
-- FROM raw_input

select *
from raw_input
