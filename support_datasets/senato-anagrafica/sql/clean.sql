-- clean.sql — senato_anagrafica
-- Anagrafica senatori (XIX legislatura, graph composizione/19).
-- Input: query SPARQL (una riga = un senatore, GROUP BY + MAX).
--
-- Normalizzazioni:
--   - senatore_id: estrazione numerica dall'URI /senatore/N
--   - nome/cognome: split della label "Nome Cognome" (prima parola = nome)
--   - data_nascita: già ISO dal sorgente (bio:date)
--   - luogo_nascita: label della città di nascita (nodeID risolto nella query)
--   - legislatura: costante 19 (perimetro XIX; estensione 13-19 = lavoro futuro)

WITH base AS (
    SELECT * FROM raw_input
)
SELECT
    TRY_CAST(regexp_extract(senatore, '/senatore/(\d+)', 1) AS BIGINT) AS senatore_id,
    normalize_string(split_part(normalize_string(label), ' ', 1))      AS nome,
    normalize_string(
        CASE
            WHEN strpos(normalize_string(label), ' ') > 0
            THEN substring(normalize_string(label), strpos(normalize_string(label), ' ') + 1)
            ELSE NULL
        END
    )                                                                   AS cognome,
    TRY_CAST(dataNascita AS DATE)                                       AS data_nascita,
    normalize_string(citta)                                             AS luogo_nascita,
    19                                                                  AS legislatura
FROM base
WHERE senatore IS NOT NULL
