-- clean.sql — mef_rappresentanti_partecipate
--
-- Input: CSV MEF con encoding ISO-8859-1, delimitatore ;
-- Schema uniforme per anni 2017-2023.
-- Le colonne oltre la 30 sono vuote/scarto.

WITH raw_clean AS (
    SELECT
        -- Amministrazione
        TRIM(CAST("Amministrazione Denominazione" AS VARCHAR))           AS amministrazione,
        TRIM(CAST("Amministrazione Settore Istituzionale" AS VARCHAR))  AS amm_settore,
        TRIM(CAST("Amministrazione Macrocategoria" AS VARCHAR))         AS amm_macrocategoria,
        TRIM(CAST("Amministrazione Categoria" AS VARCHAR))              AS amm_categoria,
        TRIM(CAST("Amministrazione Codice Fiscale" AS VARCHAR))         AS amm_cf,
        TRIM(CAST("Amministrazione Regione Sede" AS VARCHAR))           AS amm_regione,
        TRIM(CAST("Amministrazione Provincia Sede" AS VARCHAR))         AS amm_provincia,
        TRIM(CAST("Amministrazione Comune Sede" AS VARCHAR))            AS amm_comune,

        -- Società partecipata
        TRIM(CAST("Società/ente in cui è nominato il rappresentante Denominazione" AS VARCHAR)) AS societa,
        TRIM(CAST("Società/Ente Codice Fiscale" AS VARCHAR))            AS societa_cf,
        TRY_CAST(TRIM(CAST("Società/Ente Anno di costituzione" AS VARCHAR)) AS INTEGER) AS societa_anno_costituzione,
        TRIM(CAST("Società/Ente Forma Giuridica" AS VARCHAR))           AS societa_forma_giuridica,
        TRIM(CAST("Società/Ente Stato Giuridico" AS VARCHAR))           AS societa_stato,
        TRIM(CAST("Società/Ente Settore Attività" AS VARCHAR))          AS societa_settore,
        TRIM(CAST("Società/Ente Divisione ATECO" AS VARCHAR))           AS societa_ateco,
        TRIM(CAST("Società/Ente Regione Sede" AS VARCHAR))              AS societa_regione,
        TRIM(CAST("Società/Ente Provincia Sede" AS VARCHAR))            AS societa_provincia,
        TRIM(CAST("Società/Ente Comune Sede" AS VARCHAR))               AS societa_comune,

        -- Rappresentante
        TRY_CAST(TRIM(CAST("Rappresentante identificativo" AS VARCHAR)) AS BIGINT) AS rapp_id,
        TRIM(CAST("Rappresentante Cognome" AS VARCHAR))                 AS rapp_cognome,
        TRIM(CAST("Rappresentante Nome" AS VARCHAR))                    AS rapp_nome,
        TRIM(CAST("Rappresentante Genere" AS VARCHAR))                  AS rapp_genere,

        -- Incarico
        TRIM(CAST("Incarico Tipologia" AS VARCHAR))                     AS incarico_tipo,
        TRIM(CAST("Incarico Data inizio" AS VARCHAR))                   AS incarico_data_inizio,
        TRIM(CAST("Incarico Data fine" AS VARCHAR))                     AS incarico_data_fine,
        TRIM(CAST("Incarico gratuito o remunerato" AS VARCHAR))         AS incarico_gratuito,
        -- Importo: formato italiano (punto come separatore migliaia, virgola come decimale)
        TRY_CAST(REPLACE(
            REPLACE(TRIM(CAST("Incarico Importo trattamento economico" AS VARCHAR)), '.', ''),
            ',', '.'
        ) AS DOUBLE)                                                    AS incarico_importo_eur,
        TRY_CAST(REPLACE(
            REPLACE(TRIM(CAST("Incarico Compenso riversato all'Amministrazione" AS VARCHAR)), '.', ''),
            ',', '.'
        ) AS DOUBLE)                                                    AS incarico_riversato_eur

    FROM raw_input
    WHERE "Rappresentante identificativo" IS NOT NULL
)

SELECT
    amministrazione, amm_settore, amm_macrocategoria, amm_categoria,
    amm_cf, amm_regione, amm_provincia, amm_comune,
    societa, societa_cf, societa_anno_costituzione,
    societa_forma_giuridica, societa_stato, societa_settore, societa_ateco,
    societa_regione, societa_provincia, societa_comune,
    rapp_id, rapp_cognome, rapp_nome, rapp_genere,
    incarico_tipo, incarico_data_inizio, incarico_data_fine,
    incarico_gratuito, incarico_importo_eur, incarico_riversato_eur
FROM raw_clean
WHERE
    rapp_id IS NOT NULL
    AND rapp_cognome IS NOT NULL
