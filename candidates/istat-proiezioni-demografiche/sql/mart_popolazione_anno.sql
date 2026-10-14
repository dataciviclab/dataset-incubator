-- Mart: popolazione proiettata (componente=popolazione_inizio_anno)
-- Grano: territorio × anno
SELECT
    anno,
    territorio_codice,
    territorio,
    valore AS popolazione
FROM clean_input
WHERE componente_codice = 'popolazione_inizio_anno'
  AND valore IS NOT NULL
ORDER BY territorio_codice, anno
