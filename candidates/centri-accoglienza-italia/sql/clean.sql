-- Centri di accoglienza per migranti (CAS, CPA, Hotspot) — clean
-- Fonte: Centri d'Italia (ActionAid Italia + Fondazione Openpolis), CC-BY 4.0
-- Un record = un centro x convenzione in una data di rilevazione (uno snapshot
-- per anno, al 31/12); `anno` derivato da rilevazione_data. Lo stesso `centro_id`
-- compare piu' volte (piu' convenzioni/contratti con capienza e date diverse).
--
-- SELECT DISTINCT rimuove le righe esatte duplicate della fonte (206 su 47.419,
-- concentrate nel 2023-2024: stesso centro, stessa convenzione, stessi valori).

SELECT DISTINCT
    CAST(substr(CAST("rilevazione_data" AS VARCHAR), 1, 4) AS INTEGER) AS anno,
    trim(CAST("rilevazione_data" AS VARCHAR)) AS rilevazione_data,
    TRY_CAST("centro_id" AS BIGINT) AS centro_id,
    trim(CAST("centro_denominazione" AS VARCHAR)) AS centro_denominazione,
    TRY_CAST("comune_id" AS BIGINT) AS comune_id,
    trim(CAST("comune_denominazione" AS VARCHAR)) AS comune_denominazione,
    TRY_CAST("comune_codice_istat" AS BIGINT) AS comune_codice_istat,
    TRY_CAST("comune_abitanti" AS BIGINT) AS comune_abitanti,
    trim(CAST("comune_codice_catastale" AS VARCHAR)) AS comune_codice_catastale,
    TRY_CAST("provincia_cm_id" AS BIGINT) AS provincia_cm_id,
    trim(CAST("provincia_cm_denominazione" AS VARCHAR)) AS provincia_cm_denominazione,
    TRY_CAST("provincia_cm_codice_istat" AS BIGINT) AS provincia_cm_codice_istat,
    TRY_CAST("provincia_cm_abitanti" AS BIGINT) AS provincia_cm_abitanti,
    trim(CAST("provincia_cm_sigla" AS VARCHAR)) AS provincia_cm_sigla,
    TRY_CAST("regione_id" AS BIGINT) AS regione_id,
    trim(CAST("regione_denominazione" AS VARCHAR)) AS regione_denominazione,
    TRY_CAST("regione_codice_istat" AS BIGINT) AS regione_codice_istat,
    TRY_CAST("regione_abitanti" AS BIGINT) AS regione_abitanti,
    trim(CAST("ente_gestore" AS VARCHAR)) AS ente_gestore,
    TRY_CAST("data_stipula_convenzione" AS DATE) AS data_stipula_convenzione,
    TRY_CAST("data_scadenza_convenzione" AS DATE) AS data_scadenza_convenzione,
    TRY_CAST("data_scadenza_proroga" AS DATE) AS data_scadenza_proroga,
    TRY_CAST("costo_giornaliero_per_ospite" AS DOUBLE) AS costo_giornaliero_per_ospite,
    TRY_CAST("presenze_giornaliere" AS BIGINT) AS presenze_giornaliere,
    TRY_CAST("capienza" AS BIGINT) AS capienza,
    trim(CAST("procedura_affidamento" AS VARCHAR)) AS procedura_affidamento,
    trim(CAST("operativita" AS VARCHAR)) AS operativita,
    trim(CAST("tipologia_centro" AS VARCHAR)) AS tipologia_centro,
    trim(CAST("tipologia_ospiti" AS VARCHAR)) AS tipologia_ospiti
FROM raw_input
