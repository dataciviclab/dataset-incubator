SELECT
    cast_int(SUBSTR(AnnoA, 1, 4)) AS anno,
    normalize_string(AteneoCOD) AS ateneo_cod,
    normalize_string(AteneoNOME) AS ateneo_nome,
    normalize_string(SESSO) AS sesso,
    cast_int(Isc) AS iscritti
FROM raw_input
WHERE
    TRY_cast_int(SUBSTR(AnnoA, 1, 4)) IS NOT NULL
    AND cast_int(Isc) IS NOT NULL
    AND Isc >= 0
