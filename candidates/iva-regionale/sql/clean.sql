-- clean.sql — iva_regionale
-- Volume d'affari IVA per regione. Valori raw in migliaia di euro,
-- convertiti in euro (×1000) per confronto con IRPEF.
-- Numeri raw in formato italiano (punti migliaia, virgola decimale):
-- normalizzati con le macro standard (normalize_italian_integer per i
-- conteggi, normalize_italian_number per gli ammontari).
-- Le Frequenze indicano quante partite IVA dichiarano ciascuna voce:
-- fondamentali per calcoli pro-capite corretti e per l'analisi
-- contribuenti a credito vs a debito.

WITH raw_parsed AS (
    SELECT
        CAST({year} - 1 AS INTEGER)                                 AS anno,
        normalize_string("Regione")                                 AS regione,
        LPAD(normalize_string("Codice"), 2, '0')                    AS cod_regione,
        normalize_italian_integer("Numero contribuenti IVA")        AS contribuenti,
        normalize_italian_integer("Volume d'affari - Frequenza")    AS volume_frequenza,
        normalize_italian_number("Volume d'affari - Ammontare")     AS _va,
        normalize_italian_integer("Totale acquisti ed importazioni - Frequenza") AS acquisti_frequenza,
        normalize_italian_number("Totale acquisti ed importazioni - Ammontare") AS _acq,
        normalize_italian_integer("Valore aggiunto fiscale - Frequenza") AS va_frequenza,
        normalize_italian_number("Valore aggiunto fiscale - Ammontare") AS _vaf,
        normalize_italian_integer("Imposta dovuta - Frequenza")     AS imposta_dovuta_frequenza,
        normalize_italian_number("Imposta dovuta - Ammontare")      AS _imp_dov,
        normalize_italian_integer("Imposta a credito - Frequenza")  AS imposta_credito_frequenza,
        normalize_italian_number("Imposta a credito - Ammontare")   AS _imp_cred
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
