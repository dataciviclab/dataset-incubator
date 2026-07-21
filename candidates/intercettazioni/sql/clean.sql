-- clean.sql — Intercettazioni: bersagli per tipologia, ufficio e distretto
-- Fonte: Ministero della Giustizia — DG Statistica (Intercettazioni.xlsx)
-- Sheet: "Tutti gli uffici"
--
-- NOTA: schema da verificare all'apertura del file.

SELECT
    cast_int("Anno") AS anno,
    normalize_string("Tipo ufficio") AS tipo_ufficio,
    normalize_string("Distretto") AS distretto,
    normalize_string("Tipologia di intercettazione") AS tipologia_intercettazione,
    cast_int("Numero di bersagli") AS n_bersagli
FROM raw_input
