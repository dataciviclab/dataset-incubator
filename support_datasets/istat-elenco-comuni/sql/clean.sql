-- Seleziona e normalizza le colonne dal CSV raw unificato
SELECT
    codice_istat,
    denominazione,
    codice_catastale,
    CAST(superficie_km2 AS DOUBLE) AS superficie_km2,
    CAST(popolazione_residente AS INTEGER) AS popolazione_residente,
    CAST(popolazione_legale AS INTEGER) AS popolazione_legale,
    regione,
    provincia,
    sigla_provincia,
    CAST(zona_altimetrica AS INTEGER) AS zona_altimetrica,
    CAST(altitudine AS INTEGER) AS altitudine,
    CAST(comune_litoraneo AS BOOLEAN) AS comune_litoraneo,
    CAST(comune_isolano AS BOOLEAN) AS comune_isolano
FROM raw_input
ORDER BY codice_istat
