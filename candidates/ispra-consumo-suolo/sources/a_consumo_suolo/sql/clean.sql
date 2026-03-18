-- clean.sql — ispra_consumo_suolo
--
-- Input: foglio Comuni_2006_2024 dal file XLSX ISPRA (rilascio 2025, anni 2006-2024)
-- La riga 0 del foglio contiene header ISPRA originali.
-- Colonne selezionate (perimetro minimo v0):
--   pro_com                  — codice ISTAT comune (6 cifre: 3 provincia + 3 comune)
--   comune                   — nome comune
--   provincia                — nome provincia
--   regione                  — nome regione
--   incremento_ha_2023_2024  — incremento netto consumo suolo 2023-2024 [ettari]
--   stock_ha_2024            — suolo consumato cumulato 2024 [ettari]
--   stock_pct_2024           — suolo consumato 2024 [% superficie]
--
-- Nomi colonne verificati sul file reale (rilascio 2025): unita = [ettari], non [ha].

SELECT
    CAST(TRIM(CAST("PRO_COM" AS VARCHAR))               AS VARCHAR) AS pro_com,
    TRIM(CAST("Nome_Comune"   AS VARCHAR))               AS comune,
    TRIM(CAST("Nome_Provincia" AS VARCHAR))              AS provincia,
    TRIM(CAST("Nome_Regione"   AS VARCHAR))              AS regione,
    TRY_CAST(
        REPLACE(
            TRIM(CAST("Incremento netto 2023-2024 [ettari]" AS VARCHAR)), ',', '.'
        ) AS DOUBLE
    )                                                    AS incremento_ha_2023_2024,
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
