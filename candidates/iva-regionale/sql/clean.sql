-- clean.sql — iva_regionale
-- Volume d'affari IVA per regione. Valori raw in migliaia di euro,
-- convertiti in euro (×1000) per confronto con IRPEF.

WITH raw_parsed AS (
    SELECT
        {year}::INTEGER                                             AS anno,
        TRIM(CAST("Regione" AS VARCHAR))                            AS regione,
        LPAD(TRIM(CAST("Codice" AS VARCHAR)), 2, '0')               AS cod_regione,
        TRY_CAST("Numero contribuenti IVA" AS BIGINT)               AS contribuenti,
        TRY_CAST("Volume d'affari - Ammontare" AS DOUBLE)           AS _va,
        TRY_CAST("Totale acquisti ed importazioni - Ammontare" AS DOUBLE) AS _acq,
        TRY_CAST("Valore aggiunto fiscale - Ammontare" AS DOUBLE)   AS _vaf,
        TRY_CAST("Imposta dovuta - Ammontare" AS DOUBLE)            AS _imp_dov,
        TRY_CAST("Imposta a credito - Ammontare" AS DOUBLE)         AS _imp_cred
    FROM raw_input
    WHERE "Regione" IS NOT NULL AND "Codice" IS NOT NULL
)
SELECT
    anno, regione, cod_regione, contribuenti,
    ROUND(_va * 1000, 0)       AS volume_affari_eur,
    ROUND(_acq * 1000, 0)      AS acquisti_eur,
    ROUND(_vaf * 1000, 0)      AS va_fiscale_eur,
    ROUND(_imp_dov * 1000, 0)  AS imposta_dovuta_eur,
    ROUND(_imp_cred * 1000, 0) AS imposta_credito_eur
FROM raw_parsed
