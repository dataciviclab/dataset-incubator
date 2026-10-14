-- Mart: popolazione proiettata per regione × sesso × età × anno
-- Solo dettaglio (escluso sesso=totale e eta=Totale per evitare doppioni)
SELECT
    territorio_codice,
    anno,
    sesso,
    eta,
    popolazione
FROM clean_input
WHERE sesso != 'totale'
  AND eta != 'Totale'
ORDER BY territorio_codice, sesso, eta, anno
