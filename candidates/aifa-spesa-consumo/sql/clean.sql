-- clean.sql - aifa_spesa_consumo
-- Input: CSV pipe-separated, header presente
-- Output: raw-faithful, nessun filtro applicato
--   - Tutte le righe hanno spesa_convenzionata valorizzata (verificato su 2018-2024)
--   - Unico rename: TRIM su tutte le colonne stringa

SELECT
    CAST(anno AS INTEGER)                                   AS anno,
    CAST(mese AS INTEGER)                                   AS mese,
    TRIM(CAST(codreg AS VARCHAR))                            AS codreg,
    TRIM(CAST(regione AS VARCHAR))                           AS regione,
    TRIM(CAST(classe AS VARCHAR))                            AS classe,
    TRIM(CAST(atc1 AS VARCHAR))                              AS atc1,
    TRIM(CAST(descrizione_atc1 AS VARCHAR))                 AS descrizione_atc1,
    TRIM(CAST(atc2 AS VARCHAR))                             AS atc2,
    TRIM(CAST(descrizione_atc2 AS VARCHAR))                 AS descrizione_atc2,
    TRIM(CAST(atc3 AS VARCHAR))                             AS atc3,
    TRIM(CAST(descrizione_atc3 AS VARCHAR))                  AS descrizione_atc3,
    TRIM(CAST(atc4 AS VARCHAR))                              AS atc4,
    TRIM(CAST(descrizione_atc4 AS VARCHAR))                 AS descrizione_atc4,
    TRY_CAST(numero_confezioni_traccia AS DOUBLE)           AS numero_confezioni_traccia,
    TRY_CAST(spesa_flusso_tracciabilita AS DOUBLE)         AS spesa_flusso_tracciabilita,
    TRY_CAST(numero_confezioni_convenzionata AS DOUBLE)     AS numero_confezioni_convenzionata,
    TRY_CAST(spesa_convenzionata AS DOUBLE)                  AS spesa_convenzionata
FROM raw_input
