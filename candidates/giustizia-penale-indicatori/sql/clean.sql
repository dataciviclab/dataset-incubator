-- Clean layer: Giustizia penale - clearance rate e disposition time
-- 4 sheet unificati: Tribunali, Corti d'Appello, Giudici di Pace, Minorenni
-- Fonte: Ministero della Giustizia (Indicatori_Penali.xlsx)
-- V0: solo sheet "Tribunali"

SELECT
    cast_int("Anno") AS anno,
    normalize_string("Tipo ufficio") AS tipo_ufficio,
    normalize_string("Distretto") AS distretto,
    normalize_string("Sede") AS sede,
    normalize_string("Sezione") AS sezione,
    cast_double("Clearance rate") AS clearance_rate,
    cast_double("Disposition time") AS disposition_time_gg
FROM raw_input
WHERE cast_int("Anno") IS NOT NULL
  AND cast_double("Clearance rate") IS NOT NULL
