-- Clean layer: Giustizia penale - clearance rate e disposition time
-- Sheet: Tribunali
-- Fonte: Ministero della Giustizia
SELECT
    TRY_CAST("Anno" AS INTEGER)         AS anno,
    TRIM("Tipo ufficio")                AS tipo_ufficio,
    TRIM("Distretto")                   AS distretto,
    TRIM("Sede")                        AS sede,
    TRIM("Sezione")                     AS sezione,
    TRY_CAST("Clearance rate" AS DOUBLE)    AS clearance_rate,
    TRY_CAST("Disposition time" AS DOUBLE) AS disposition_time_gg
FROM raw_input
WHERE TRY_CAST("Anno" AS INTEGER) IS NOT NULL;
