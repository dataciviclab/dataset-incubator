-- clean.sql — camera_gruppi
-- Gruppi parlamentari della Camera (tutte le legislature).
-- Input: query SPARQL (una riga = un gruppo, già dedup con GROUP BY + MAX).
--
-- Normalizzazioni:
--   - legislatura: URI ocd/legislatura.rdf/repubblica_17 → "repubblica_17"
--   - label: stringa, trim (contiene nome + acronimo + date di esistenza)

WITH base AS (
    SELECT * FROM raw_input
)
SELECT
    normalize_string(gruppo)                                             AS gruppo,
    normalize_string(label)                                              AS nome,
    CASE
        WHEN legislatura LIKE '%/legislatura.rdf/%' THEN
            substring(legislatura, strpos(legislatura, '/legislatura.rdf/') + 17)
        ELSE legislatura
    END                                                                  AS legislatura
FROM base
WHERE gruppo IS NOT NULL
