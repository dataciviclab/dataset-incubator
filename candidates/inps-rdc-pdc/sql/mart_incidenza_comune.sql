-- mart_incidenza_comune — Incidenza RdC/PdC per comune
--
-- 1 riga = 1 comune ISTAT: nuclei RdC/PdC, popolazione, takeup (metrica
-- ufficiale INPS) e incidenza ricalcolata (nuclei/popolazione).
-- Serve per: comuni con incidenza più alta (domanda guida README),
-- join con IRPEF e altri indicatori socio-economici.
-- NOTA: esclude i comuni con popolazione 0 (codici ISTAT soppressi/fusi).
--
-- PK: (codice_istat)

SELECT
    codice_istat,
    comune,
    codice_regione,
    codice_provincia,
    nuclei_rdc,
    nuclei_pdc,
    nuclei_rdc + nuclei_pdc AS nuclei_tot,
    individui_coinvolti,
    importo_medio_mensile,
    popolazione_residente,
    takeup,
    ROUND(100.0 * (nuclei_rdc + nuclei_pdc) / NULLIF(popolazione_residente, 0), 2) AS incidenza_rdc_pct
FROM clean_input
WHERE popolazione_residente > 0
ORDER BY incidenza_rdc_pct DESC
