-- mart_top_comuni — Top comuni per incidenza e per nuclei
--
-- 1 riga = 1 comune (popolazione > 0): incidenza RdC/PdC, nuclei totali,
-- importo medio, rank per incidenza e per nuclei.
-- Serve per: benchmark territoriale, comuni con povertà più concentrata.
--
-- PK: (codice_istat)

WITH base AS (
    SELECT
        codice_istat,
        comune,
        codice_regione,
        nuclei_rdc,
        nuclei_pdc,
        nuclei_rdc + nuclei_pdc AS nuclei_tot,
        importo_medio_mensile,
        popolazione_residente,
        ROUND(100.0 * (nuclei_rdc + nuclei_pdc) / NULLIF(popolazione_residente, 0), 2) AS incidenza_rdc_pct
    FROM clean_input
    WHERE popolazione_residente > 0
)
SELECT
    codice_istat,
    comune,
    codice_regione,
    nuclei_rdc,
    nuclei_pdc,
    nuclei_tot,
    importo_medio_mensile,
    incidenza_rdc_pct,
    ROW_NUMBER() OVER (ORDER BY incidenza_rdc_pct DESC) AS rank_incidenza,
    ROW_NUMBER() OVER (ORDER BY nuclei_tot DESC) AS rank_nuclei
FROM base
ORDER BY rank_incidenza
