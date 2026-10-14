-- clean.sql: proiezioni demografiche ISTAT base 2025 → 2080
-- Canale: SDMX IT1/165_889 (DCIS_PREVDEM1)
-- Macros toolkit: normalize_string / cast_int / cast_double
--
-- Filtri: solo IT + regioni NUTS2, scenario mediano (se disponibile),
-- popolazione residente (non età quinquennale se troppo granulare).
-- Le dimensioni esatte dipendono dal DSD: adattare dopo primo run.

SELECT
    cast_int(TIME_PERIOD) AS anno,
    normalize_string(REF_AREA) AS territorio_codice,
    CASE normalize_string(REF_AREA)
        WHEN 'IT' THEN 'Italia'
        WHEN 'ITC' THEN 'Nord-Ovest'
        WHEN 'ITH' THEN 'Nord-Est'
        WHEN 'ITI' THEN 'Centro'
        WHEN 'ITF' THEN 'Sud'
        WHEN 'ITG' THEN 'Isole'
        WHEN 'ITC1' THEN 'Piemonte'
        WHEN 'ITC2' THEN "Valle d'Aosta"
        WHEN 'ITC3' THEN 'Liguria'
        WHEN 'ITC4' THEN 'Lombardia'
        WHEN 'ITH1' THEN 'P.A. Bolzano'
        WHEN 'ITH2' THEN 'P.A. Trento'
        WHEN 'ITH3' THEN 'Veneto'
        WHEN 'ITH4' THEN 'Friuli-Venezia Giulia'
        WHEN 'ITH5' THEN 'Emilia-Romagna'
        WHEN 'ITI1' THEN 'Toscana'
        WHEN 'ITI2' THEN 'Umbria'
        WHEN 'ITI3' THEN 'Marche'
        WHEN 'ITI4' THEN 'Lazio'
        WHEN 'ITF1' THEN 'Abruzzo'
        WHEN 'ITF2' THEN 'Molise'
        WHEN 'ITF3' THEN 'Campania'
        WHEN 'ITF4' THEN 'Puglia'
        WHEN 'ITF5' THEN 'Basilicata'
        WHEN 'ITF6' THEN 'Calabria'
        WHEN 'ITG1' THEN 'Sicilia'
        WHEN 'ITG2' THEN 'Sardegna'
        ELSE normalize_string(REF_AREA)
    END AS territorio,
    CASE normalize_string(SEX)
        WHEN '1' THEN 'maschi'
        WHEN '2' THEN 'femmine'
        WHEN '9' THEN 'totale'
        ELSE normalize_string(SEX)
    END AS sesso,
    -- età: se il raw usa classi quinquennali o totale, normalizza
    normalize_string(AGE) AS eta,
    cast_double(OBS_VALUE) AS popolazione
FROM raw_input
WHERE cast_int(TIME_PERIOD) IS NOT NULL
  AND normalize_string(REF_AREA) IS NOT NULL
  AND cast_double(OBS_VALUE) IS NOT NULL
  -- filtro scenario/mediano da adattare dopo primo run (colonna dipende dal DSD)
  -- esempio: AND normalize_string(SCENARIO) = 'MED'
