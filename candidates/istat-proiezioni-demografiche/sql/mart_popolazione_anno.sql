-- Mart: popolazione proiettata per età × sesso × regione × anno
-- Grano: territorio × sesso × età × anno (scenario mediano)
SELECT
    anno,
    territorio_codice,
    sesso,
    eta,
    valore AS popolazione
FROM clean_input
WHERE grano = 'eta_sesso'
  AND componente_codice = 'popolazione'
  AND sesso != 'totale'  -- escludi totali sesso (duplicati)
  AND eta != 'Totale'    -- escludi totali età (duplicati)
  AND valore IS NOT NULL
ORDER BY territorio_codice, sesso, eta, anno
