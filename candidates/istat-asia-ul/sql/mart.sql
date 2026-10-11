SELECT
    codice_comune,
    anno,
    ateco_sezione,
    ROUND(unita_locali, 0) AS unita_locali
FROM clean_input
WHERE
    codice_comune IS NOT NULL
    AND anno IS NOT NULL
    AND ateco_sezione IS NOT NULL
    AND unita_locali IS NOT NULL
