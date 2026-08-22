-- Mart scadenze: bandi aperti per data di scadenza (prossime, dall'ultima passata in avanti)
SELECT
    data_scadenza,
    COUNT(*)        AS num_bandi,
    SUM(num_posti)  AS posti_totali
FROM clean_input
WHERE status = 'OPEN'
  AND data_scadenza IS NOT NULL
GROUP BY data_scadenza
ORDER BY data_scadenza
