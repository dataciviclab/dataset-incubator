-- clean.sql - aifa_spesa_consumo
-- Perimetro: solo flusso convenzionata (prescrizioni SSN dispensate in farmacia)
-- Input: CSV pipe-separated, UTF-8-BOM, header presente
-- Nomi colonna verificati sul file reale 2023.
--
-- Filtro convenzionata: righe con spesa_convenzionata non vuota.
-- I valori vuoti nelle colonne tracciabilita sulle stesse righe sono strutturali, non errori.
-- 2023: ~92.6k righe convenzionata su ~174.6k totali.

SELECT
    CAST(anno AS INTEGER)                                  AS anno,
    CAST(mese AS INTEGER)                                  AS mese,
    TRIM(CAST(codreg AS VARCHAR))                          AS codreg,
    TRIM(CAST(regione AS VARCHAR))                         AS regione,
    TRIM(CAST(classe AS VARCHAR))                          AS classe,
    TRIM(CAST(atc1 AS VARCHAR))                            AS atc1,
    TRIM(CAST(descrizione_atc1 AS VARCHAR))                AS descrizione_atc1,
    TRIM(CAST(atc2 AS VARCHAR))                            AS atc2,
    TRIM(CAST(descrizione_atc2 AS VARCHAR))                AS descrizione_atc2,
    TRIM(CAST(atc3 AS VARCHAR))                            AS atc3,
    TRIM(CAST(descrizione_atc3 AS VARCHAR))                AS descrizione_atc3,
    TRIM(CAST(atc4 AS VARCHAR))                            AS atc4,
    TRIM(CAST(descrizione_atc4 AS VARCHAR))                AS descrizione_atc4,
    TRY_CAST(numero_confezioni_convenzionata AS DOUBLE)    AS numero_confezioni_convenzionata,
    TRY_CAST(spesa_convenzionata AS DOUBLE)                AS spesa_convenzionata
FROM raw_input
WHERE TRY_CAST(spesa_convenzionata AS DOUBLE) IS NOT NULL
  AND TRY_CAST(anno AS INTEGER) IS NOT NULL
