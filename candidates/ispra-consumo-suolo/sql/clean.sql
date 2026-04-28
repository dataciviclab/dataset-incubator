-- clean.sql — ispra_consumo_suolo
--
-- Input: foglio Comuni_2006_2024 dal file XLSX ISPRA (rilascio 2025, anni 2006-2024)
-- La riga 0 del foglio contiene header ISPRA originali.
--
-- Colonne selezionate (39 raw cols -> 39 clean cols, tutte preservate):
--   Identificativi:     pro_com / comune / provincia / regione
--   Incrementi netti:   incremento_netto_ha_<periodo>
--   Incrementi lordi:   incremento_lordo_ha_<periodo>
--   Ripristini:         ripristino_ha_<periodo>         (prima scartate, ora incluse)
--   Stock:              stock_ha_2024 / stock_pct_2024
--
-- Razionale: le colonne Ripristino sono parte della serie storica ISPRA.
-- Non sono state scartate per ragioni analitiche ma per errore di omissione.
-- Ora incluse in clean per preservazione raw-faithful.

SELECT
    CAST(TRIM(CAST("PRO_COM" AS VARCHAR)) AS VARCHAR) AS pro_com,
    TRIM(CAST("Nome_Comune"   AS VARCHAR))               AS comune,
    TRIM(CAST("Nome_Provincia" AS VARCHAR))              AS provincia,
    TRIM(CAST("Nome_Regione"   AS VARCHAR))              AS regione,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Incremento netto 2006-2012 [ettari]" AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS incremento_netto_ha_2006_2012,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Incremento lordo 2006-2012 [ettari]" AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS incremento_lordo_ha_2006_2012,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Ripristino 2006-2012 [ettari]" AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS ripristino_ha_2006_2012,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Incremento netto 2012-2015 [ettari]" AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS incremento_netto_ha_2012_2015,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Incremento lordo 2012-2015 [ettari]" AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS incremento_lordo_ha_2012_2015,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Ripristino 2012-2015 [ettari]" AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS ripristino_ha_2012_2015,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Incremento netto 2015-2016 [ettari]" AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS incremento_netto_ha_2015_2016,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Incremento lordo 2015-2016 [ettari]" AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS incremento_lordo_ha_2015_2016,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Ripristino 2015-2016 [ettari]" AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS ripristino_ha_2015_2016,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Incremento netto 2016-2017 [ettari]" AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS incremento_netto_ha_2016_2017,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Incremento lordo 2016-2017 [ettari]" AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS incremento_lordo_ha_2016_2017,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Ripristino 2016-2017 [ettari]" AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS ripristino_ha_2016_2017,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Incremento netto 2017-2018 [ettari]" AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS incremento_netto_ha_2017_2018,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Incremento lordo 2017-2018 [ettari]" AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS incremento_lordo_ha_2017_2018,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Ripristino 2017-2018 [ettari]" AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS ripristino_ha_2017_2018,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Incremento netto 2018-2019 [ettari]" AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS incremento_netto_ha_2018_2019,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Incremento lordo 2018-2019 [ettari]" AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS incremento_lordo_ha_2018_2019,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Ripristino 2018-2019 [ettari]" AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS ripristino_ha_2018_2019,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Incremento netto 2019-2020 [ettari]" AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS incremento_netto_ha_2019_2020,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Incremento lordo 2019-2020 [ettari]" AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS incremento_lordo_ha_2019_2020,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Ripristino 2019-2020 [ettari]" AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS ripristino_ha_2019_2020,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Incremento netto 2020-2021 [ettari]" AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS incremento_netto_ha_2020_2021,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Incremento lordo 2020-2021 [ettari]" AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS incremento_lordo_ha_2020_2021,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Ripristino 2020-2021 [ettari]" AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS ripristino_ha_2020_2021,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Incremento netto 2021-2022 [ettari]" AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS incremento_netto_ha_2021_2022,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Incremento lordo 2021-2022 [ettari]" AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS incremento_lordo_ha_2021_2022,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Ripristino 2021-2022 [ettari]" AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS ripristino_ha_2021_2022,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Incremento netto 2022-2023 [ettari]" AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS incremento_netto_ha_2022_2023,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Incremento lordo 2022-2023 [ettari]" AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS incremento_lordo_ha_2022_2023,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Ripristino 2022-2023 [ettari]" AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS ripristino_ha_2022_2023,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Incremento netto 2023-2024 [ettari]" AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS incremento_ha_2023_2024,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Incremento netto 2023-2024 [ettari]" AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS incremento_netto_ha_2023_2024,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Incremento lordo 2023-2024 [ettari]" AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS incremento_lordo_ha_2023_2024,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Ripristino 2023-2024 [ettari]" AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS ripristino_ha_2023_2024,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Suolo consumato 2024 [ettari]"  AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS stock_ha_2024,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Suolo consumato 2024 [%]"   AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS stock_pct_2024

FROM raw_input

WHERE
    "PRO_COM" IS NOT NULL
    AND TRY_CAST("PRO_COM" AS INTEGER) IS NOT NULL
