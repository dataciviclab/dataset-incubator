-- Top call UE per importo contrattato (beneficiari Italia, no RRF).
-- call_id è popolato solo dal 2025 nel sorgente FTS — anni precedenti
-- non generano righe utili (tutte N/A → NULL).
SELECT
    call_id,
    COUNT(*) AS n_grant,
    COUNT(DISTINCT beneficiario_nome) AS n_beneficiari,
    SUM(importo_contrattato) AS importo_contrattato_totale,
    AVG(importo_contrattato) AS importo_medio,
    MIN(data_inizio_progetto) AS data_inizio_min,
    MAX(data_fine_progetto) AS data_fine_max
FROM clean_input
WHERE call_id IS NOT NULL
  AND is_rrf = 'NO'
  AND importo_contrattato IS NOT NULL
GROUP BY call_id
ORDER BY importo_contrattato_totale DESC
