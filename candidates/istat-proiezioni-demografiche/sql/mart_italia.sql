-- Mart: popolazione proiettata Italia (somma delle regioni)
-- Esclude ITH (Trentino-Alto Adige aggregato) per evitare doppio conteggio
-- con ITH1 (Bolzano) e ITH2 (Trento) — presenti tutti e tre nel ZIP.
-- Grano: sesso × età × anno
SELECT
    anno,
    sesso,
    eta,
    sum(popolazione) AS popolazione
FROM clean_input
WHERE sesso != 'totale'
  AND eta != 'Totale'
  AND territorio_codice != 'ITH'  -- aggregato, duplica ITH1+ITH2
GROUP BY anno, sesso, eta
ORDER BY sesso, eta, anno
