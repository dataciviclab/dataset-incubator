-- clean.sql - aifa_spesa_consumo
-- Input: CSV pipe-separated, header presente
-- Output: raw-faithful con normalizzazione denominazioni regionali
--   - TRIM su tutte le colonne stringa
--   - Normalizzazione nomi regione (fonte AIFA troncata in alcuni anni)

SELECT
    CAST(anno AS INTEGER)                                   AS anno,
    CAST(mese AS INTEGER)                                   AS mese,
    TRIM(CAST(codreg AS VARCHAR))                            AS codreg,
    CASE
        WHEN TRIM(CAST(regione AS VARCHAR)) IN ('LOMBARDI')                              THEN 'LOMBARDIA'
        WHEN TRIM(CAST(regione AS VARCHAR)) IN ('VALLE D''')                             THEN 'VALLE D''AOSTA'
        WHEN TRIM(CAST(regione AS VARCHAR)) IN ('PA BOLZA', 'PA BOLZANO')                THEN 'PROVINCIA DI BOLZANO'
        WHEN TRIM(CAST(regione AS VARCHAR)) IN ('PA TRENT', 'PA TRENTO')                THEN 'PROVINCIA DI TRENTO'
        WHEN TRIM(CAST(regione AS VARCHAR)) IN ('FRIULI V', 'FRIULI VENEZIA GIULIA')     THEN 'FRIULI-VENEZIA GIULIA'
        WHEN TRIM(CAST(regione AS VARCHAR)) IN ('EMILIA R', 'EMILIA ROMAGNA')           THEN 'EMILIA-ROMAGNA'
        WHEN TRIM(CAST(regione AS VARCHAR)) IN ('BASILICA')                              THEN 'BASILICATA'
        ELSE TRIM(CAST(regione AS VARCHAR))
    END                                                      AS regione,
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
