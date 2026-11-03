-- MASE SISEN — "Consumi petroliferi, dati definitivi" (annuale).
-- File: Consumi_Petroliferi_Definitivi_YYYY.xlsx, foglio "CONSUMI PETROLIFERI".
-- Layout: report a blocchi affiancati (I° SEMESTRE a sx, 2° SEMESTRE a dx).
--   riga 1 = titolo, riga 2 = anno, riga 3 = intestazioni semestre, riga 4 = mesi
--   -> read.skip=4 + header=false: le colonne sono posizionali, nominate col0..col26.
--   col0 = prodotto (etichetta solo sulla prima riga del blocco, poi celle vuote o
--          marcatori "DI CUI:" / "=") -> forward-fill che ignora i marcatori.
--   col1 = dettaglio.
--   Colonne mese (non cumulative): col2,col3,col5,col7,col9,col11 (GEN..GIU) e
--                                  col15,col17,col19,col21,col23,col25 (LUG..DIC).
--   Le colonne cumulative (GEN.FEB, GEN.MAR, ...) sono ignorate.
-- Unità: migliaia di tonnellate (,000 tonn.).
-- Estratti i prodotti principali (non le voci "di cui").
--
-- Nota tipi: le colonne mese arrivano con tipi misti (VARCHAR/DOUBLE) e UNPIVOT
-- richiede tipi uniformi. `all_varchar` NON si applica al path Excel (è solo CSV),
-- quindi il cast è esplicito qui con COLUMNS(*)::VARCHAR.

WITH src AS (
    SELECT row_number() OVER () AS rn, COLUMNS(*)::VARCHAR
    FROM raw_input
),
lab AS (
    SELECT
        *,
        MAX(
            CASE
                WHEN trim(COALESCE(col0, '')) <> ''
                 AND upper(trim(col0)) NOT LIKE 'DI CUI%'
                 AND trim(col0) <> '='
                THEN rn
            END
        ) OVER (ORDER BY rn ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS prod_rn
    FROM src
),
flat AS (
    SELECT
        l.rn,
        p.col0 AS prodotto,
        NULLIF(regexp_replace(trim(COALESCE(l.col1, '')), ' +', ' ', 'g'), '') AS dettaglio,
        l.col2 AS m1,
        l.col3 AS m2,
        l.col5 AS m3,
        l.col7 AS m4,
        l.col9 AS m5,
        l.col11 AS m6,
        l.col15 AS m7,
        l.col17 AS m8,
        l.col19 AS m9,
        l.col21 AS m10,
        l.col23 AS m11,
        l.col25 AS m12
    FROM lab l
    LEFT JOIN src p ON p.rn = l.prod_rn
),
sel AS (
    SELECT *
    FROM flat
    WHERE (prodotto = 'BENZINA' AND dettaglio = 'AUTO TOTALE')
       OR (prodotto = 'CARBOTURBO' AND dettaglio = 'TOTALE (A)')
       OR (prodotto = 'GASOLIO' AND dettaglio = 'TOTALE GASOLI')
       OR (prodotto = 'OLIO COMB.LE' AND dettaglio = 'TOTALE')
       OR (prodotto IN ('LUBRIFICANTI TOTALE', 'GPL', 'BITUMI', 'TOTALE PRODOTTI PRINCIPALI')
           AND dettaglio IS NULL)
),
long AS (
    UNPIVOT sel
    ON m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12
    INTO NAME mese_col VALUE consumo_kt
)
SELECT
    {year} AS anno,
    CAST(replace(mese_col, 'm', '') AS INTEGER) AS mese,
    CASE
        WHEN prodotto = 'OLIO COMB.LE' THEN 'olio combustibile'
        WHEN prodotto = 'TOTALE PRODOTTI PRINCIPALI' THEN 'totale prodotti principali'
        WHEN prodotto = 'LUBRIFICANTI TOTALE' THEN 'lubrificanti'
        ELSE lower(prodotto)
    END AS prodotto,
    TRY_CAST(consumo_kt AS DOUBLE) AS consumo_kt
FROM long
