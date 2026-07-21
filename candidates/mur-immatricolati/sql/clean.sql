SELECT
    cast_int(SUBSTR(AnnoA, 1, 4)) AS anno,
    normalize_string(ClasseNUMERO) AS classe_cod,
    normalize_string(ClasseNOME) AS classe_nome,
    normalize_string(Sesso) AS sesso,
    cast_int(Immatricolati) AS immatricolati
FROM raw_input
WHERE
    TRY_cast_int(SUBSTR(AnnoA, 1, 4)) IS NOT NULL
    AND cast_int(Immatricolati) IS NOT NULL
    AND Immatricolati >= 0
