-- clean.sql — istat_occupazione_provinciale
--
-- Input: SDMX-CSV dai dataflow ISTAT 150_915 (tasso occupazione) e 151_914
-- (tasso disoccupazione), concatenati dal reader SDMX.
--
-- Output: formato long, una riga per provincia × anno × sesso × classe età
-- con due metriche: tasso occupazione EMP_R e tasso disoccupazione UNEM_R.

SELECT
    "REF_AREA"                                              AS ref_area,
    "REF_AREA_label"                                        AS territorio,
    TRY_CAST("TIME_PERIOD" AS INTEGER)                      AS anno,
    "DATA_TYPE"                                             AS indicatore,
    "SEX"                                                   AS sesso_codice,
    CASE "SEX"
        WHEN '1' THEN 'maschi'
        WHEN '2' THEN 'femmine'
        WHEN '9' THEN 'totale'
    END                                                     AS sesso,
    "AGE"                                                   AS eta_codice,
    "AGE_label"                                             AS eta,
    -- Tasso: OBS_VALUE è già percentuale (0-100)
    TRY_CAST("value" AS DOUBLE)                             AS valore

FROM raw_input

WHERE
    -- Solo frequenza annuale
    "FREQ" = 'A'
    -- Solo livelli territoriali provincia (codice NUTS3 a 5 caratteri)
    AND LENGTH("REF_AREA") = 5
    AND "REF_AREA" NOT LIKE 'IT%0%'   -- esclude ITC10 etc (raggruppamenti)
    -- Solo cittadinanza totale
    AND "CITIZENSHIP" = 'TOTAL'
    -- Solo istruzione totale (per v0; le singole classi available via EDU_LEV_HIGHEST)
    AND "EDU_LEV_HIGHEST" = '99'
    -- Solo classi età principali per v0
    AND "AGE" IN ('Y15-64', 'Y15-24', 'Y25-34', 'Y35-44', 'Y45-54', 'Y55-64')
    -- Solo tassi (occupazione e disoccupazione)
    AND "DATA_TYPE" IN ('EMP_R', 'UNEM_R')
    -- Anno valido
    AND TRY_CAST("TIME_PERIOD" AS INTEGER) IS NOT NULL
    -- Valore non nullo
    AND TRY_CAST("value" AS DOUBLE) IS NOT NULL
