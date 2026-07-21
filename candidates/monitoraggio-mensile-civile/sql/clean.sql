-- clean.sql — Monitoraggio mensile civile: iscritti e definiti per mese/sede/materia
-- Fonte: Ministero della Giustizia — DG Statistica (Monitoraggio_mensile.xlsx)
--
-- NOTA: schema da verificare all'apertura del file. Colonne ipotizzate
-- sulla base dell'esplorazione: Fonte, Tipo_ufficio, Anno, Mese, AnnoMese,
-- Distretto, Sede, Materia, Iscritti, Definiti, Area, Dati.

SELECT
    cast_int("Anno") AS anno,
    cast_int("Mese") AS mese,
    normalize_string("Fonte") AS fonte,
    normalize_string("Tipo ufficio") AS tipo_ufficio,
    normalize_string("Distretto") AS distretto,
    normalize_string("Sede") AS sede,
    normalize_string("Materia") AS materia,
    cast_int("Iscritti") AS iscritti,
    cast_int("Definiti") AS definiti,
    normalize_string("Area") AS area,
    normalize_string("Dati") AS flag_dato
FROM raw_input
