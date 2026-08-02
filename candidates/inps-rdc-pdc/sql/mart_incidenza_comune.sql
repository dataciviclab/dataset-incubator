-- mart_incidenza_comune — Incidenza RdC/PdC per comune
--
-- 1 riga = 1 comune: nuclei RdC/PdC, popolazione, takeup (metrica ufficiale
-- INPS), incidenza ricalcolata (nuclei/popolazione), regione e provincia.
-- Serve per: comuni con incidenza più alta (domanda guida README), join con
-- IRPEF e altri indicatori socio-economici.
-- NOTA: esclude i comuni con popolazione 0 (codici soppressi/fusi).
--
-- PK: (codice_catastale)

SELECT
    codice_catastale,
    codice_istat,
    comune,
    regione,
    sigla_provincia,
    nuclei_rdc,
    nuclei_pdc,
    nuclei_rdc + nuclei_pdc AS nuclei_tot,
    individui_coinvolti,
    importo_medio_mensile,
    superficie_km2,
    popolazione_residente,
    takeup,
    ROUND(100.0 * (nuclei_rdc + nuclei_pdc) / NULLIF(popolazione_residente, 0), 2) AS incidenza_rdc_pct,
    ROUND((nuclei_rdc + nuclei_pdc) / NULLIF(superficie_km2, 0), 2) AS nuclei_per_km2
FROM clean_input
WHERE popolazione_residente > 0
ORDER BY incidenza_rdc_pct DESC
