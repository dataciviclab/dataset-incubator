SELECT
    CAST(SUBSTR(AnnoA, 1, 4) AS INTEGER) AS anno,
    CAST(ClasseNUMERO AS VARCHAR) AS classe_cod,
    CAST(ClasseNOME AS VARCHAR) AS classe_nome,
    CAST(Sesso AS VARCHAR) AS sesso,
    TRY_CAST(Immatricolati AS INTEGER) AS immatricolati
FROM raw_input
WHERE
    TRY_CAST(SUBSTR(AnnoA, 1, 4) AS INTEGER) IS NOT NULL
    AND TRY_CAST(Immatricolati AS INTEGER) IS NOT NULL
    AND Immatricolati >= 0
