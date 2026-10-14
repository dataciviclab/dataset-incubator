-- Mart: tutte le componenti del bilancio demografico proiettato
-- Grano: territorio × componente × anno
SELECT
    anno,
    territorio_codice,
    territorio,
    componente_codice,
    componente,
    valore
FROM clean_input
WHERE componente_codice != 'popolazione_inizio_anno'
  AND valore IS NOT NULL
ORDER BY territorio_codice, componente_codice, anno
