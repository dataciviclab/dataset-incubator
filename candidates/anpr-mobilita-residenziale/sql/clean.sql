-- clean.sql — anpr_mobilita_residenziale
-- Flussi mensili di cambio residenza tra regioni italiane (ANPR)

SELECT
    cast_int(ANNO)                                       AS anno,
    cast_int(MESE)                                       AS mese,
    normalize_string(PARTENZA)                              AS partenza,
    LPAD(normalize_string(COD_ISTAT_REGIONE_DI_PARTENZA), 3, '0') AS cod_regione_partenza,
    normalize_string(ARRIVO)                                AS arrivo,
    LPAD(normalize_string(COD_ISTAT_REGIONE_DI_ARRIVO), 3, '0')   AS cod_regione_arrivo,
    cast_int(TOTALE)                                     AS totale

FROM raw_input
WHERE TOTALE IS NOT NULL
  AND ANNO IS NOT NULL
