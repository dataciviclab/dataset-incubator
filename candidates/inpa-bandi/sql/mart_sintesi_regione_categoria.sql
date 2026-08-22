-- Mart sintesi: bandi aperti per regione x categoria
SELECT
    regione,
    categoria,
    COUNT(*)        AS num_bandi,
    SUM(num_posti)  AS posti_totali
FROM clean_input
WHERE status = 'OPEN'
  AND regione IS NOT NULL
GROUP BY regione, categoria
ORDER BY num_bandi DESC, regione, categoria
