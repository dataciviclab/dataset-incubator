-- clean.sql — iva_regionale
-- Volume d'affari IVA per regione. Valori raw in migliaia di euro,
-- convertiti in euro (×1000) per confronto con IRPEF.
-- Le Frequenze indicano quante partite IVA dichiarano ciascuna voce:
-- fondamentali per calcoli pro-capite corretti e per l'analisi
-- contribuenti a credito vs a debito.
-- Macro standard: cast_bigint/cast_double/normalize_string
-- (il preprocess ha gia' normalizzato il formato numerico italiano:
--  niente normalize_italian_number).

WITH raw_parsed AS (
    SELECT
        CAST({year} - 1 AS INTEGER)                                 AS anno,
        normalize_string("Regione")                                 AS regione,
        LPAD(normalize_string("Codice"), 2, '0')                    AS cod_regione,
        cast_bigint("Numero contribuenti IVA")                      AS contribuenti,
        cast_bigint("Volume d'affari - Frequenza")                  AS volume_frequenza,
        cast_double("Volume d'affari - Ammontare")                  AS _va,
        cast_bigint("Totale acquisti ed importazioni - Frequenza")  AS acquisti_frequenza,
        cast_double("Totale acquisti ed importazioni - Ammontare")  AS _acq,
        cast_bigint("Valore aggiunto fiscale - Frequenza")          AS va_frequenza,
        cast_double("Valore aggiunto fiscale - Ammontare")          AS _vaf,
        cast_bigint("Imposta dovuta - Frequenza")                   AS imposta_dovuta_frequenza,
        cast_double("Imposta dovuta - Ammontare")                   AS _imp_dov,
        cast_bigint("Imposta a credito - Frequenza")                AS imposta_credito_frequenza,
        cast_double("Imposta a credito - Ammontare")                AS _imp_cred
    FROM raw_input
    WHERE "Regione" IS NOT NULL AND "Codice" IS NOT NULL
      AND normalize_string("Regione") NOT IN ('TOTALE', 'Non indicata')
      AND normalize_string("Codice") != ''
)
SELECT
    anno, regione, cod_regione, contribuenti,
    volume_frequenza,
    ROUND(_va * 1000, 0)       AS volume_affari_eur,
    acquisti_frequenza,
    ROUND(_acq * 1000, 0)      AS acquisti_eur,
    va_frequenza,
    ROUND(_vaf * 1000, 0)      AS va_fiscale_eur,
    imposta_dovuta_frequenza,
    ROUND(_imp_dov * 1000, 0)  AS imposta_dovuta_eur,
    imposta_credito_frequenza,
    ROUND(_imp_cred * 1000, 0) AS imposta_credito_eur
FROM raw_parsed
