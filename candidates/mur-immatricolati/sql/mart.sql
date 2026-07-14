SELECT
    anno,
    classe_cod,
    classe_nome,
    sesso,
    SUM(immatricolati) AS immatricolati
FROM clean_input
GROUP BY anno, classe_cod, classe_nome, sesso
ORDER BY anno, classe_cod, sesso
