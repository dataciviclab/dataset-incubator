SELECT
    anno,
    ateneo_cod,
    ateneo_nome,
    sesso,
    SUM(iscritti) AS iscritti
FROM clean_input
GROUP BY anno, ateneo_cod, ateneo_nome, sesso
ORDER BY anno, ateneo_cod, sesso
