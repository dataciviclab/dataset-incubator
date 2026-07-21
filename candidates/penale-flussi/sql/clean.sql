-- clean.sql — Penale Flussi: iscritti, definiti, pendenti per ufficio penale
-- Fonte: Ministero della Giustizia — DG Statistica (PenaleFlussi*.xlsx)
--
-- NOTA: schema da verificare all'apertura del file. Questo è un template
-- basato sulla struttura attesa (analoga a CivileFlussi ma per il penale).

SELECT
    {year}::INTEGER AS anno,
    normalize_string("fonte") AS fonte,
    normalize_string("tipo_ufficio") AS tipo_ufficio,
    normalize_string("distretto") AS distretto,
    normalize_string("sede") AS sede,
    normalize_string("macromateria") AS macromateria,
    normalize_string("materia") AS materia,
    normalize_string("dettaglio") AS dettaglio,
    cast_int("iscritti") AS iscritti,
    cast_int("definiti") AS definiti_totale,
    cast_int("pendenti") AS pendenti_finali
FROM raw_input
