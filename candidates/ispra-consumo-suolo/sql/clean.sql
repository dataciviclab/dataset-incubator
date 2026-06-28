-- clean.sql — ispra_consumo_suolo (formato long)
--
-- Input: foglio Comuni_2006_2024 dal file XLSX ISPRA (rilascio 2025, anni 2006-2024)
--
-- Trasformazione: passa da wide (una colonna per periodo) a long (una riga
-- per comune × periodo). Ricostruisce inoltre lo stock (suolo consumato
-- cumulato) per ogni anno finale di periodo, partendo da stock_2024 noto e
-- sottraendo gli incrementi netti successivi.
--
-- Output: ~87.000 righe (7.896 comuni × 11 periodi), 11 colonne.
--
-- Periodi:
--   Pluriennali: 2006-2012, 2012-2015  (stock ricostruito all'anno finale)
--   Annuali:     2015-2016, 2016-2017, …, 2023-2024
--
-- Colonne output:
--   pro_com, comune, provincia, regione  (identificativi)
--   periodo                               (es. "2015-2016")
--   anno                                  (anno finale, per JOIN e ordinamento)
--   incremento_netto_ha                   (flusso netto nel periodo)
--   incremento_lordo_ha                   (flusso lordo nel periodo)
--   ripristino_ha                         (aree recuperate nel periodo)
--   stock_ha                              (stock cumulato a fine periodo, ricostruito)
--   stock_pct                             (stock percentuale a fine periodo, ricostruito)

WITH wide AS (
    SELECT
        CAST(TRIM(CAST("PRO_COM" AS VARCHAR)) AS VARCHAR)                             AS pro_com,
        TRIM(CAST("Nome_Comune"   AS VARCHAR))                                        AS comune,
        TRIM(CAST("Nome_Provincia" AS VARCHAR))                                       AS provincia,
        TRIM(CAST("Nome_Regione"   AS VARCHAR))                                       AS regione,

        TRY_CAST(REPLACE(TRIM(CAST("Incremento netto 2006-2012 [ettari]" AS VARCHAR)), ',', '.') AS DOUBLE) AS inc_netto_2006_2012,
        TRY_CAST(REPLACE(TRIM(CAST("Incremento lordo 2006-2012 [ettari]" AS VARCHAR)), ',', '.') AS DOUBLE) AS inc_lordo_2006_2012,
        TRY_CAST(REPLACE(TRIM(CAST("Ripristino 2006-2012 [ettari]" AS VARCHAR)), ',', '.') AS DOUBLE)     AS ripristino_2006_2012,

        TRY_CAST(REPLACE(TRIM(CAST("Incremento netto 2012-2015 [ettari]" AS VARCHAR)), ',', '.') AS DOUBLE) AS inc_netto_2012_2015,
        TRY_CAST(REPLACE(TRIM(CAST("Incremento lordo 2012-2015 [ettari]" AS VARCHAR)), ',', '.') AS DOUBLE) AS inc_lordo_2012_2015,
        TRY_CAST(REPLACE(TRIM(CAST("Ripristino 2012-2015 [ettari]" AS VARCHAR)), ',', '.') AS DOUBLE)     AS ripristino_2012_2015,

        TRY_CAST(REPLACE(TRIM(CAST("Incremento netto 2015-2016 [ettari]" AS VARCHAR)), ',', '.') AS DOUBLE) AS inc_netto_2015_2016,
        TRY_CAST(REPLACE(TRIM(CAST("Incremento lordo 2015-2016 [ettari]" AS VARCHAR)), ',', '.') AS DOUBLE) AS inc_lordo_2015_2016,
        TRY_CAST(REPLACE(TRIM(CAST("Ripristino 2015-2016 [ettari]" AS VARCHAR)), ',', '.') AS DOUBLE)     AS ripristino_2015_2016,

        TRY_CAST(REPLACE(TRIM(CAST("Incremento netto 2016-2017 [ettari]" AS VARCHAR)), ',', '.') AS DOUBLE) AS inc_netto_2016_2017,
        TRY_CAST(REPLACE(TRIM(CAST("Incremento lordo 2016-2017 [ettari]" AS VARCHAR)), ',', '.') AS DOUBLE) AS inc_lordo_2016_2017,
        TRY_CAST(REPLACE(TRIM(CAST("Ripristino 2016-2017 [ettari]" AS VARCHAR)), ',', '.') AS DOUBLE)     AS ripristino_2016_2017,

        TRY_CAST(REPLACE(TRIM(CAST("Incremento netto 2017-2018 [ettari]" AS VARCHAR)), ',', '.') AS DOUBLE) AS inc_netto_2017_2018,
        TRY_CAST(REPLACE(TRIM(CAST("Incremento lordo 2017-2018 [ettari]" AS VARCHAR)), ',', '.') AS DOUBLE) AS inc_lordo_2017_2018,
        TRY_CAST(REPLACE(TRIM(CAST("Ripristino 2017-2018 [ettari]" AS VARCHAR)), ',', '.') AS DOUBLE)     AS ripristino_2017_2018,

        TRY_CAST(REPLACE(TRIM(CAST("Incremento netto 2018-2019 [ettari]" AS VARCHAR)), ',', '.') AS DOUBLE) AS inc_netto_2018_2019,
        TRY_CAST(REPLACE(TRIM(CAST("Incremento lordo 2018-2019 [ettari]" AS VARCHAR)), ',', '.') AS DOUBLE) AS inc_lordo_2018_2019,
        TRY_CAST(REPLACE(TRIM(CAST("Ripristino 2018-2019 [ettari]" AS VARCHAR)), ',', '.') AS DOUBLE)     AS ripristino_2018_2019,

        TRY_CAST(REPLACE(TRIM(CAST("Incremento netto 2019-2020 [ettari]" AS VARCHAR)), ',', '.') AS DOUBLE) AS inc_netto_2019_2020,
        TRY_CAST(REPLACE(TRIM(CAST("Incremento lordo 2019-2020 [ettari]" AS VARCHAR)), ',', '.') AS DOUBLE) AS inc_lordo_2019_2020,
        TRY_CAST(REPLACE(TRIM(CAST("Ripristino 2019-2020 [ettari]" AS VARCHAR)), ',', '.') AS DOUBLE)     AS ripristino_2019_2020,

        TRY_CAST(REPLACE(TRIM(CAST("Incremento netto 2020-2021 [ettari]" AS VARCHAR)), ',', '.') AS DOUBLE) AS inc_netto_2020_2021,
        TRY_CAST(REPLACE(TRIM(CAST("Incremento lordo 2020-2021 [ettari]" AS VARCHAR)), ',', '.') AS DOUBLE) AS inc_lordo_2020_2021,
        TRY_CAST(REPLACE(TRIM(CAST("Ripristino 2020-2021 [ettari]" AS VARCHAR)), ',', '.') AS DOUBLE)     AS ripristino_2020_2021,

        TRY_CAST(REPLACE(TRIM(CAST("Incremento netto 2021-2022 [ettari]" AS VARCHAR)), ',', '.') AS DOUBLE) AS inc_netto_2021_2022,
        TRY_CAST(REPLACE(TRIM(CAST("Incremento lordo 2021-2022 [ettari]" AS VARCHAR)), ',', '.') AS DOUBLE) AS inc_lordo_2021_2022,
        TRY_CAST(REPLACE(TRIM(CAST("Ripristino 2021-2022 [ettari]" AS VARCHAR)), ',', '.') AS DOUBLE)     AS ripristino_2021_2022,

        TRY_CAST(REPLACE(TRIM(CAST("Incremento netto 2022-2023 [ettari]" AS VARCHAR)), ',', '.') AS DOUBLE) AS inc_netto_2022_2023,
        TRY_CAST(REPLACE(TRIM(CAST("Incremento lordo 2022-2023 [ettari]" AS VARCHAR)), ',', '.') AS DOUBLE) AS inc_lordo_2022_2023,
        TRY_CAST(REPLACE(TRIM(CAST("Ripristino 2022-2023 [ettari]" AS VARCHAR)), ',', '.') AS DOUBLE)     AS ripristino_2022_2023,

        TRY_CAST(REPLACE(TRIM(CAST("Incremento netto 2023-2024 [ettari]" AS VARCHAR)), ',', '.') AS DOUBLE) AS inc_netto_2023_2024,
        TRY_CAST(REPLACE(TRIM(CAST("Incremento lordo 2023-2024 [ettari]" AS VARCHAR)), ',', '.') AS DOUBLE) AS inc_lordo_2023_2024,
        TRY_CAST(REPLACE(TRIM(CAST("Ripristino 2023-2024 [ettari]" AS VARCHAR)), ',', '.') AS DOUBLE)     AS ripristino_2023_2024,

        TRY_CAST(REPLACE(TRIM(CAST("Suolo consumato 2024 [ettari]" AS VARCHAR)), ',', '.') AS DOUBLE)     AS stock_ha_2024,
        TRY_CAST(REPLACE(TRIM(CAST("Suolo consumato 2024 [%]" AS VARCHAR)), ',', '.') AS DOUBLE)           AS stock_pct_2024

    FROM raw_input

    WHERE
        "PRO_COM" IS NOT NULL
        AND TRY_CAST("PRO_COM" AS INTEGER) IS NOT NULL
),

-- Superficie comunale in ettari (calcolata dallo stock 2024)
superficie AS (
    SELECT
        pro_com,
        ROUND(stock_ha_2024 / NULLIF(stock_pct_2024, 0) * 100, 4) AS sup_ha,
        stock_ha_2024,
        stock_pct_2024
    FROM wide
),

-- Unpivot: da wide (una colonna per periodo) a long (una riga per periodo)
long AS (
    SELECT pro_com, '2006-2012' AS periodo, 2012 AS anno,
        inc_netto_2006_2012 AS incremento_netto_ha,
        inc_lordo_2006_2012 AS incremento_lordo_ha,
        ripristino_2006_2012 AS ripristino_ha
    FROM wide WHERE inc_netto_2006_2012 IS NOT NULL
    UNION ALL
    SELECT pro_com, '2012-2015', 2015,
        inc_netto_2012_2015, inc_lordo_2012_2015, ripristino_2012_2015
    FROM wide WHERE inc_netto_2012_2015 IS NOT NULL
    UNION ALL
    SELECT pro_com, '2015-2016', 2016,
        inc_netto_2015_2016, inc_lordo_2015_2016, ripristino_2015_2016
    FROM wide WHERE inc_netto_2015_2016 IS NOT NULL
    UNION ALL
    SELECT pro_com, '2016-2017', 2017,
        inc_netto_2016_2017, inc_lordo_2016_2017, ripristino_2016_2017
    FROM wide WHERE inc_netto_2016_2017 IS NOT NULL
    UNION ALL
    SELECT pro_com, '2017-2018', 2018,
        inc_netto_2017_2018, inc_lordo_2017_2018, ripristino_2017_2018
    FROM wide WHERE inc_netto_2017_2018 IS NOT NULL
    UNION ALL
    SELECT pro_com, '2018-2019', 2019,
        inc_netto_2018_2019, inc_lordo_2018_2019, ripristino_2018_2019
    FROM wide WHERE inc_netto_2018_2019 IS NOT NULL
    UNION ALL
    SELECT pro_com, '2019-2020', 2020,
        inc_netto_2019_2020, inc_lordo_2019_2020, ripristino_2019_2020
    FROM wide WHERE inc_netto_2019_2020 IS NOT NULL
    UNION ALL
    SELECT pro_com, '2020-2021', 2021,
        inc_netto_2020_2021, inc_lordo_2020_2021, ripristino_2020_2021
    FROM wide WHERE inc_netto_2020_2021 IS NOT NULL
    UNION ALL
    SELECT pro_com, '2021-2022', 2022,
        inc_netto_2021_2022, inc_lordo_2021_2022, ripristino_2021_2022
    FROM wide WHERE inc_netto_2021_2022 IS NOT NULL
    UNION ALL
    SELECT pro_com, '2022-2023', 2023,
        inc_netto_2022_2023, inc_lordo_2022_2023, ripristino_2022_2023
    FROM wide WHERE inc_netto_2022_2023 IS NOT NULL
    UNION ALL
    SELECT pro_com, '2023-2024', 2024,
        inc_netto_2023_2024, inc_lordo_2023_2024, ripristino_2023_2024
    FROM wide WHERE inc_netto_2023_2024 IS NOT NULL
),

-- Ricostruzione stock: per ogni periodo, stock_ha = stock_2024 - somma
-- degli incrementi netti di TUTTI i periodi con anno > anno_corrente.
con_stock AS (
    SELECT
        l.pro_com,
        w.comune,
        w.provincia,
        w.regione,
        l.periodo,
        l.anno,
        l.incremento_netto_ha,
        l.incremento_lordo_ha,
        l.ripristino_ha,
        -- Somma cumulativa degli incrementi netti dal periodo corrente al 2024
        SUM(l.incremento_netto_ha) OVER (
            PARTITION BY l.pro_com
            ORDER BY l.anno DESC
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS cum_inc_da_2024,
        s.stock_ha_2024,
        s.sup_ha
    FROM long l
    JOIN wide w USING (pro_com)
    JOIN superficie s USING (pro_com)
)

SELECT
    pro_com,
    comune,
    provincia,
    regione,
    periodo,
    anno,
    ROUND(incremento_netto_ha, 4)   AS incremento_netto_ha,
    ROUND(incremento_lordo_ha, 4)   AS incremento_lordo_ha,
    ROUND(ripristino_ha, 4)         AS ripristino_ha,
    -- stock_ha = stock_2024 - somma incrementi successivi al periodo corrente
    ROUND(stock_ha_2024 - (cum_inc_da_2024 - incremento_netto_ha), 2) AS stock_ha,
    ROUND((stock_ha_2024 - (cum_inc_da_2024 - incremento_netto_ha)) / NULLIF(sup_ha, 0) * 100, 4) AS stock_pct

FROM con_stock
ORDER BY pro_com, anno DESC
