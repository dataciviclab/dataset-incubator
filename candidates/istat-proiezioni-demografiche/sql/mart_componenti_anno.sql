-- Mart: componenti bilancio demografico proiettato
-- Grano: territorio × componente × anno (Italia + ripartizioni + regioni)
SELECT
    anno,
    territorio_codice,
    componente_codice,
    valore
FROM clean_input
WHERE grano = 'componenti'
  AND valore IS NOT NULL
ORDER BY territorio_codice, componente_codice, anno
