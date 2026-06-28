-- mart.sql — istat_occupazione_provinciale
-- mart_occupazione_provinciale: dati pass-through (long format già pronto)

SELECT
    ref_area,
    territorio,
    anno,
    indicatore,
    sesso_codice,
    sesso,
    eta_codice,
    eta,
    ROUND(valore, 2) AS valore

FROM clean_input

WHERE
    ref_area IS NOT NULL
    AND anno IS NOT NULL
    AND valore IS NOT NULL
