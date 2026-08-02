-- clean.sql — inps_rdc_pdc
-- Nuclei familiari percettori RdC/PdC per comune ISTAT (luglio 2020).
-- Snapshot unico INPS Open Data. Valori numerici già parsati da DuckDB
-- (read.decimal='.'), quindi cast diretto con macro standard.
-- NOTA: i nomi colonna raw hanno caratteri speciali (<, >, ., -) che
-- richiedono quoting doppio nel SELECT.

SELECT
    {year}::INTEGER                                            AS anno,
    normalize_string("codice_istat")                           AS codice_istat,
    normalize_string("Comune")                                 AS comune,
    cast_int("Codice_Regione")                                 AS codice_regione,
    cast_int("Codice_Provincia")                               AS codice_provincia,
    cast_double("Nuclei_familiari_percettori_RDC_luglio_2020") AS nuclei_rdc,
    cast_double("Nuclei_familiari_percettori_PDC_luglio_2020") AS nuclei_pdc,
    cast_double("Individui_coinvolti_luglio_2020")             AS individui_coinvolti,
    cast_double("Numero_componenti_per_famiglia")              AS componenti_per_famiglia,
    cast_double("Numero_donne_per_famiglia")                   AS donne_per_famiglia,
    cast_double("Numero_minori_<_18_anni_per_famiglia")        AS minori_18_per_famiglia,
    cast_double("Numero_anziani_>_75_anni_per_famiglia")       AS anziani_75_per_famiglia,
    cast_double("Importo_medio_mensile")                       AS importo_medio_mensile,
    cast_double("Dev.standard_importo_mensile")                AS dev_standard_importo,
    cast_double("Uomini_residenti_al_1-1-2020")                AS uomini_residenti,
    cast_double("Donne_residenti_al_1-1-2020")                 AS donne_residenti,
    cast_double("Popolazione_residente_al_1-1-2020")           AS popolazione_residente,
    cast_double("Takeup")                                      AS takeup,
    cast_double("Takeup_donne")                                AS takeup_donne
FROM raw_input
WHERE "codice_istat" IS NOT NULL AND "codice_istat" != ''
