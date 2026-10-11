-- clean.sql — AMECO: previsioni macro della Commissione UE (Spring 2026)
--
-- Perimetro lean: 6 serie chiave × 6 paesi/aggregati.
-- Raw: 18 CSV wide (CODE, COUNTRY, SUB-CHAPTER, TITLE, UNIT, 1960..2027, Unnamed: 73).
-- Output: long format (paese × serie × anno).
--
-- Variante unità per serie (dal CODE: PAESE.a.b.UNIT.c.SERIES):
--   ZUTN   unit=0   → tasso disoccupazione % popolazione attiva
--   UVGD   unit=99  → PIL nominale Mrd ECU/EUR
--   UBLG   unit=319 → saldo netto govt %PIL (EDP)
--   UDGG   unit=319 → debito consolidato govt %PIL (EDP)
--   UBLGAP unit=319 → saldo ciclicamente aggiustato %PIL potenziale
--   ADGGI  unit=0   → snowball effect debito %PIL EDP

WITH filtered AS (
    SELECT *
    EXCLUDE ("SUB-CHAPTER", "Unnamed: 73")
    FROM raw_input
    WHERE
        -- 6 paesi / aggregati peer
        split_part(CODE, '.', 1) IN ('ITA', 'DEU', 'FRA', 'ESP', 'EU27', 'EA20')
        -- 6 serie con unità specifica (esclude varianti tipo UBLGAPS, unità PPS, ecc.)
        AND (
            (split_part(CODE, '.', 6) = 'ZUTN'  AND split_part(CODE, '.', 4) = '0')
            OR (split_part(CODE, '.', 6) = 'UVGD'  AND split_part(CODE, '.', 4) = '99')
            OR (split_part(CODE, '.', 6) = 'UBLG'  AND split_part(CODE, '.', 4) = '319')
            OR (split_part(CODE, '.', 6) = 'UDGG'  AND split_part(CODE, '.', 4) = '319')
            OR (split_part(CODE, '.', 6) = 'UBLGAP' AND split_part(CODE, '.', 4) = '319')
            OR (split_part(CODE, '.', 6) = 'ADGGI' AND split_part(CODE, '.', 4) = '0')
        )
),
unpivoted AS (
    UNPIVOT filtered
    ON COLUMNS(* EXCLUDE (CODE, COUNTRY, TITLE, UNIT))
    INTO NAME anno VALUE raw_valore
)
SELECT
    split_part(CODE, '.', 1) AS paese,
    COUNTRY AS paese_nome,
    split_part(CODE, '.', 6) AS serie,
    TITLE AS titolo,
    UNIT AS unita,
    TRY_CAST(anno AS INTEGER) AS anno,
    CASE
        WHEN raw_valore IN ('NA', '') THEN NULL
        ELSE TRY_CAST(raw_valore AS DOUBLE)
    END AS valore,
    -- Spring 2026: 2025+ sono previsioni ECFIN, non osservati
    CASE
        WHEN TRY_CAST(anno AS INTEGER) >= 2025 THEN 'previsione'
        ELSE 'osservato'
    END AS tipo_dato
FROM unpivoted
WHERE
    -- solo colonne-anno (scarta residui non numerici)
    anno ~ '^[0-9]{4}$'
    AND TRY_CAST(anno AS INTEGER) BETWEEN 1960 AND 2027
    -- es righe senza dato (NA)
    AND raw_valore NOT IN ('NA', '')
