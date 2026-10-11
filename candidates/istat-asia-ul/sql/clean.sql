SELECT
    CAST(ref_area AS VARCHAR(6))            AS codice_comune,
    CAST(anno AS INTEGER)                   AS anno,
    CAST(ateco_sezione AS VARCHAR(5))       AS ateco_sezione,
    CAST(valore AS DOUBLE)                  AS unita_locali
FROM raw_input
WHERE
    LENGTH(ref_area) = 6
    AND TRY_CAST(ref_area AS INTEGER) IS NOT NULL
    AND anno IS NOT NULL
    AND anno BETWEEN 2018 AND 2020
    AND valore >= 0
    AND valore IS NOT NULL
