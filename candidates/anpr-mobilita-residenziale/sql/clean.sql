-- clean.sql — anpr_mobilita_residenziale
-- Flussi mensili di cambio residenza tra regioni italiane (ANPR)

SELECT
    CAST(ANNO AS INTEGER)                                       AS anno,
    CAST(MESE AS INTEGER)                                       AS mese,
    TRIM(CAST(PARTENZA AS VARCHAR))                              AS partenza,
    LPAD(TRIM(CAST(COD_ISTAT_REGIONE_DI_PARTENZA AS VARCHAR)), 3, '0') AS cod_regione_partenza,
    TRIM(CAST(ARRIVO AS VARCHAR))                                AS arrivo,
    LPAD(TRIM(CAST(COD_ISTAT_REGIONE_DI_ARRIVO AS VARCHAR)), 3, '0')   AS cod_regione_arrivo,
    CAST(TOTALE AS INTEGER)                                     AS totale

FROM raw_input
WHERE TOTALE IS NOT NULL
  AND ANNO IS NOT NULL
