-- clean.sql — inps_rdc_pdc
-- Nuclei familiari percettori RdC/PdC per comune (luglio 2020).
-- Snapshot unico INPS Open Data.
--
-- NOTA IMPORTANTE: la colonna "codice_istat" del CSV INPS è in realtà il
-- codice CATASTALE Belfiore (es. A001 = Abano Terme), non il codice ISTAT.
-- Il join con istat_elenco_comuni avviene su codice_catastale e porta:
--   - codice_istat (ISTAT 6 cifre) + sigla_provincia (da mart_codici_catastali)
--   - regione + superficie_km2 (da mart_superficie)
-- I nomi colonna raw con caratteri speciali (<, >, ., -) richiedono quoting.

WITH inps AS (
    SELECT
        UPPER(normalize_string("codice_istat"))             AS codice_catastale,
        normalize_string("Comune")                          AS comune,
        cast_int("Codice_Regione")                          AS codice_regione,
        cast_int("Codice_Provincia")                        AS codice_provincia,
        cast_double("Nuclei_familiari_percettori_RDC_luglio_2020") AS nuclei_rdc,
        cast_double("Nuclei_familiari_percettori_PDC_luglio_2020") AS nuclei_pdc,
        cast_double("Individui_coinvolti_luglio_2020")      AS individui_coinvolti,
        cast_double("Numero_componenti_per_famiglia")       AS componenti_per_famiglia,
        cast_double("Numero_donne_per_famiglia")            AS donne_per_famiglia,
        cast_double("Numero_minori_<_18_anni_per_famiglia") AS minori_18_per_famiglia,
        cast_double("Numero_anziani_>_75_anni_per_famiglia") AS anziani_75_per_famiglia,
        cast_double("Importo_medio_mensile")                AS importo_medio_mensile,
        cast_double("Dev.standard_importo_mensile")         AS dev_standard_importo,
        cast_double("Uomini_residenti_al_1-1-2020")         AS uomini_residenti,
        cast_double("Donne_residenti_al_1-1-2020")          AS donne_residenti,
        cast_double("Popolazione_residente_al_1-1-2020")    AS popolazione_residente,
        cast_double("Takeup")                               AS takeup,
        cast_double("Takeup_donne")                         AS takeup_donne
    FROM raw_input
    WHERE "codice_istat" IS NOT NULL AND "codice_istat" != ''
),
codici AS (
    SELECT codice_istat, UPPER(codice_catastale) AS codice_catastale, sigla_provincia
    FROM read_parquet('{root}/data/mart/istat_elenco_comuni/2026/mart_codici_catastali.parquet')
),
superficie AS (
    SELECT codice_istat, regione, superficie_km2
    FROM read_parquet('{root}/data/mart/istat_elenco_comuni/2026/mart_superficie.parquet')
)
SELECT
    {year}::INTEGER AS anno,
    i.codice_catastale,
    c.codice_istat,
    i.comune,
    s.regione,
    c.sigla_provincia,
    i.codice_regione,
    i.codice_provincia,
    s.superficie_km2,
    i.nuclei_rdc,
    i.nuclei_pdc,
    i.individui_coinvolti,
    i.componenti_per_famiglia,
    i.donne_per_famiglia,
    i.minori_18_per_famiglia,
    i.anziani_75_per_famiglia,
    i.importo_medio_mensile,
    i.dev_standard_importo,
    i.uomini_residenti,
    i.donne_residenti,
    i.popolazione_residente,
    i.takeup,
    i.takeup_donne
FROM inps i
LEFT JOIN codici c ON c.codice_catastale = i.codice_catastale
LEFT JOIN superficie s ON s.codice_istat = c.codice_istat
