-- SAI Strutture (Sistema Accoglienza e Integrazione) — clean
-- Fonte: Centri d'Italia (ActionAid Italia + Fondazione Openpolis), CC-BY 4.0
-- Un record = una struttura SAI a una data di rilevazione; `anno` derivato da data_rilevazione.

SELECT
    CAST(substr(CAST("data_rilevazione" AS VARCHAR), 1, 4) AS INTEGER) AS anno,
    TRY_CAST("sai_struttura_id" AS BIGINT) AS sai_struttura_id,
    trim(CAST("sai_struttura_denominazione" AS VARCHAR)) AS sai_struttura_denominazione,
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
    trim(CAST("sai_struttura_tipologia" AS VARCHAR)) AS sai_struttura_tipologia,
    trim(CAST("sai_progetto_codice" AS VARCHAR)) AS sai_progetto_codice,
    trim(CAST("sai_progetto_denominazione" AS VARCHAR)) AS sai_progetto_denominazione,
    trim(CAST("sai_progetto_tipologia" AS VARCHAR)) AS sai_progetto_tipologia,
    TRY_CAST("data_inizio" AS DATE) AS data_inizio,
    trim(CAST("data_fine" AS VARCHAR)) AS data_fine,
    TRY_CAST("data_rilevazione" AS DATE) AS data_rilevazione,
    TRY_CAST("capienza" AS BIGINT) AS capienza,
    TRY_CAST("presenze_giornaliere" AS BIGINT) AS presenze_giornaliere
FROM raw_input
