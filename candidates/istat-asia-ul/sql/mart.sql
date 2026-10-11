-- Mart ASIA UL: unità locali + addetti per comune × ATECO × anno
-- clean_input include già denominazione, regione, sigla_provincia dal JOIN in clean.sql

SELECT
    codice_comune,
    anno,
    ateco_sezione,
    ROUND(MAX(CASE WHEN data_type = 'LU' THEN valore END), 0) AS unita_locali,
    ROUND(MAX(CASE WHEN data_type = 'LUEMPDAA' THEN valore END), 0) AS addetti,
    -- colonne territoriali (una riga per group, prendo il primo valore non-null)
    MAX(denominazione)     AS denominazione,
    MAX(regione)           AS regione,
    MAX(sigla_provincia)   AS sigla_provincia
FROM clean_input
WHERE
    codice_comune IS NOT NULL
    AND anno IS NOT NULL
    AND ateco_sezione IS NOT NULL
GROUP BY codice_comune, anno, ateco_sezione
ORDER BY codice_comune, anno, ateco_sezione
