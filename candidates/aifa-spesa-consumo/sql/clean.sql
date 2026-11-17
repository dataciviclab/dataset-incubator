-- clean.sql - aifa_spesa_consumo
-- Input: CSV pipe-separated, header presente, 17 colonne (2016-2025)
-- Output: raw-faithful con normalizzazione delle stringhe
--   - TRIM su tutte le colonne stringa; stringa vuota -> NULL (macro normalize_string)
--   - 0xA0 (NBSP) rimosso: la fonte lo mette in testa/coda a descrizione_atc3/atc4
--     e TRIM da solo non lo toglie, quindi il valore resterebbe "sporco"
--   - Normalizzazione nomi regione (la fonte li tronca in alcuni anni)
--   - Nessuna aggregazione: tutto il lavoro analitico sta nel mart

WITH src AS (
    SELECT
        cast_int("anno")                                             AS anno,
        cast_int("mese")                                             AS mese,
        normalize_string("codreg")                                   AS codreg,
        normalize_string("regione")                                  AS regione,
        normalize_string("classe")                                   AS classe,
        normalize_string("atc1")                                     AS atc1,
        normalize_string(replace("descrizione_atc1", chr(160), ' ')) AS descrizione_atc1,
        normalize_string("atc2")                                     AS atc2,
        normalize_string(replace("descrizione_atc2", chr(160), ' ')) AS descrizione_atc2,
        normalize_string("atc3")                                     AS atc3,
        normalize_string(replace("descrizione_atc3", chr(160), ' ')) AS descrizione_atc3,
        normalize_string("atc4")                                     AS atc4,
        normalize_string(replace("descrizione_atc4", chr(160), ' ')) AS descrizione_atc4,
        cast_double("numero_confezioni_traccia")                     AS numero_confezioni_traccia,
        cast_double("spesa_flusso_tracciabilita")                    AS spesa_flusso_tracciabilita,
        cast_double("numero_confezioni_convenzionata")               AS numero_confezioni_convenzionata,
        cast_double("spesa_convenzionata")                           AS spesa_convenzionata
    FROM raw_input
)
SELECT
    anno,
    mese,
    codreg,
    CASE
        WHEN regione IN ('LOMBARDI')                          THEN 'LOMBARDIA'
        WHEN regione IN ('VALLE D''')                         THEN 'VALLE D''AOSTA'
        WHEN regione IN ('PA BOLZA', 'PA BOLZANO')            THEN 'PROVINCIA DI BOLZANO'
        WHEN regione IN ('PA TRENT', 'PA TRENTO')             THEN 'PROVINCIA DI TRENTO'
        WHEN regione IN ('FRIULI V', 'FRIULI VENEZIA GIULIA') THEN 'FRIULI-VENEZIA GIULIA'
        WHEN regione IN ('EMILIA R', 'EMILIA ROMAGNA')        THEN 'EMILIA-ROMAGNA'
        WHEN regione IN ('BASILICA')                          THEN 'BASILICATA'
        ELSE regione
    END                                                          AS regione,
    classe,
    atc1,
    descrizione_atc1,
    atc2,
    descrizione_atc2,
    atc3,
    descrizione_atc3,
    atc4,
    descrizione_atc4,
    numero_confezioni_traccia,
    spesa_flusso_tracciabilita,
    numero_confezioni_convenzionata,
    spesa_convenzionata
FROM src
