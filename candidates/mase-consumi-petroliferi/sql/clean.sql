-- MASE SISEN — consumi petroliferi, dati definitivi.
-- Input: raw_input.csv prodotto da preprocess.py (serie già normalizzata):
--   anno, prodotto, dettaglio, mese, consumo_kt
-- Il preprocess ha: risolto l'anno dal titolo del foglio (alcuni file ne
-- contengono più di uno), normalizzato le etichette prodotto (che cambiano
-- tra le ere: CARBOT./CARBOTURBO, OLIO COMB.LE/OLIO COMBUSTIBILE, G.P.L./GPL, …)
-- e allineato le varianti della riga di totale a `TOTALE`.
-- Qui si selezionano le voci di sintesi (non le ripartizioni "di cui").
-- Unità: migliaia di tonnellate (,000 tonn.).

SELECT
    TRY_CAST(NULLIF(TRIM(anno), '') AS INTEGER) AS anno,
    TRY_CAST(NULLIF(TRIM(mese), '') AS INTEGER) AS mese,
    prodotto,
    TRY_CAST(NULLIF(TRIM(consumo_kt), '') AS DOUBLE) AS consumo_kt
FROM raw_input
WHERE (prodotto = 'benzina' AND dettaglio = 'AUTO TOTALE')
   OR (prodotto IN ('carboturbo', 'gasolio', 'olio combustibile') AND dettaglio = 'TOTALE')
   OR (
        prodotto IN ('lubrificanti', 'gpl', 'bitumi', 'totale prodotti principali')
        AND NULLIF(TRIM(dettaglio), '') IS NULL
      )
