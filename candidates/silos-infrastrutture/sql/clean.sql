-- SILOS — Infrastrutture strategiche e prioritarie
-- Report Camera dei Deputati 2024
-- Tutte le colonne lette come VARCHAR da all_varchar, con parsing dei numeri in formato italiano

SELECT
    {year}::INTEGER AS anno,
    TRIM("Link alla scheda") AS link_scheda,
    TRY_CAST("Progressivo" AS INTEGER) AS progressivo,
    TRY_CAST("Livello" AS INTEGER) AS livello,
    TRIM("Commissariate o PNRR-PNC") AS flag_commissariato_pnrr,
    TRIM("Sistema infrastrutturale") AS sistema_infrastrutturale,
    TRIM("Cup") AS cup,
    TRIM("Denominazione") AS denominazione,
    TRIM("Soggetto competente") AS soggetto_competente,
    TRIM("Luogo lavori") AS luogo_lavori,
    TRIM("Stato di attuazione") AS stato_attuazione,
    TRY_CAST(NULLIF(TRIM("Ultimazione lavori al 31/08/2024"), '') AS INTEGER) AS anno_ultimazione_previsto,
    TRY_CAST(
        REPLACE(REPLACE(NULLIF(TRIM("Costi al 31/08/2024"), ''), '.', ''), ',', '.')
    AS DOUBLE) AS costi_mln_euro,
    TRY_CAST(
        REPLACE(REPLACE(NULLIF(TRIM("Disponibilità al 31/08/2024"), ''), '.', ''), ',', '.')
    AS DOUBLE) AS disponibilita_mln_euro,
    TRY_CAST(
        REPLACE(REPLACE(NULLIF(TRIM("Fabbisogno al 31/08/2024"), ''), '.', ''), ',', '.')
    AS DOUBLE) AS fabbisogno_mln_euro
FROM raw_input
