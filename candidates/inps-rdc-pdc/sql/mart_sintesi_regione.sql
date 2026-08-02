-- mart_sintesi_regione — Sintesi RdC/PdC per regione
--
-- 1 riga = 1 regione (codice ISTAT): comuni coperti, nuclei RdC/PdC,
-- individui coinvolti, importo medio pesato sui nuclei, incidenza media
-- (takeup medio) e popolazione totale.
-- Serve per: confronto regionale della povertà RdC/PdC, divari territoriali.
--
-- PK: (codice_regione)

SELECT
    codice_regione,
    COUNT(*) AS n_comuni,
    ROUND(SUM(nuclei_rdc), 0) AS nuclei_rdc,
    ROUND(SUM(nuclei_pdc), 0) AS nuclei_pdc,
    ROUND(SUM(nuclei_rdc + nuclei_pdc), 0) AS nuclei_tot,
    ROUND(SUM(individui_coinvolti), 0) AS individui_coinvolti,
    ROUND(
        SUM(importo_medio_mensile * (nuclei_rdc + nuclei_pdc))
        / NULLIF(SUM(nuclei_rdc + nuclei_pdc), 0),
        0
    ) AS importo_medio_pesato,
    ROUND(100.0 * AVG(takeup), 2) AS incidenza_media_pct,
    ROUND(SUM(popolazione_residente), 0) AS popolazione_totale
FROM clean_input
WHERE codice_regione IS NOT NULL
GROUP BY codice_regione
ORDER BY nuclei_tot DESC
