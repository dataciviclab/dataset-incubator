-- clean.sql — camera_incarichi
--
-- Incarichi dei deputati nei gruppi parlamentari (ruoli, date, gruppo).
-- Input: CSV da endpoint SPARQL dati.camera.it (una riga = un incarico,
-- già deduplicato con GROUP BY + MAX lato query).
--
-- Normalizzazioni:
--   - legislatura: URI ocd/legislatura.rdf/repubblica_17 → "repubblica_17"
--   - date: YYYYMMDD (BIGINT da sniff DuckDB, stringhe vuote → NULL) → DATE
--   - ruolo/label/gruppo: stringhe, trim
-- Nota: la colonna raw "end" è keyword riservata DuckDB → rinominata
-- in end_date nella CTE base (double-quote).

WITH base AS (
    SELECT
        *,
        start                                                         AS start_date,
        "end"                                                         AS end_date
    FROM raw_input
)
SELECT
    normalize_string(incarico)                                        AS incarico,
    normalize_string(ruolo)                                           AS ruolo,
    normalize_string(label)                                           AS label,
    normalize_string(deputato)                                        AS deputato,
    -- id numerico della persona dall'URI (stessa normalizzazione del
    -- candidate camera_deputati_legislature) — chiave di join standard
    TRY_CAST(
        CASE
            WHEN deputato LIKE '%/deputato.rdf/d%' AND deputato NOT LIKE '%/deputato.rdf/dr%' THEN
                regexp_extract(deputato, 'deputato\.rdf/d(\d+)_', 1)
            WHEN deputato LIKE '%/deputato.rdf/dr%' THEN
                regexp_extract(deputato, 'deputato\.rdf/dr(\d+)_', 1)
        END AS BIGINT
    )                                                                 AS persona_id,
    normalize_string(gruppo)                                          AS gruppo,
    CASE
        WHEN legislatura LIKE '%/legislatura.rdf/%' THEN
            substring(legislatura, strpos(legislatura, '/legislatura.rdf/') + 17)
        ELSE legislatura
    END                                                               AS legislatura,
    TRY_CAST(
        substr(CAST(start_date AS VARCHAR), 1, 4) || '-' ||
        substr(CAST(start_date AS VARCHAR), 5, 2) || '-' ||
        substr(CAST(start_date AS VARCHAR), 7, 2)
        AS DATE
    )                                                                 AS start_date,
    TRY_CAST(
        substr(CAST(end_date AS VARCHAR), 1, 4) || '-' ||
        substr(CAST(end_date AS VARCHAR), 5, 2) || '-' ||
        substr(CAST(end_date AS VARCHAR), 7, 2)
        AS DATE
    )                                                                 AS end_date
FROM base
WHERE incarico IS NOT NULL
