SELECT
    normalize_string(ref_area)            AS codice_comune,
    cast_int(anno)                   AS anno,
    normalize_string(ateco_sezione)       AS ateco_sezione,
    cast_double(valore)                  AS unita_locali
FROM raw_input
WHERE
    LENGTH(ref_area) = 6
    AND TRY_cast_int(ref_area) IS NOT NULL
    AND anno IS NOT NULL
    AND anno BETWEEN 2018 AND 2020
    AND valore >= 0
    AND valore IS NOT NULL
