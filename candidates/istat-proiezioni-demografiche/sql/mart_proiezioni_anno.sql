-- Mart: popolazione proiettata per territorio × sesso × età × anno
SELECT
    anno,
    territorio_codice,
    territorio,
    sesso,
    eta,
    popolazione
FROM clean_input
WHERE popolazione IS NOT NULL
ORDER BY territorio_codice, sesso, eta, anno
