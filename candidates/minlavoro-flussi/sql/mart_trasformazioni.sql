-- MinLavoro flussi — MART: trasformazioni determinato → indeterminato.
-- Fonte unica: Rapporto Annuale tabelle 03.x. Nessuna copertura in open-inps.

SELECT
    anno,
    geo_level,
    geo AS territorio,
    genere,
    SUM(valore) AS n_trasformazioni
FROM clean_input
WHERE tipo_flusso = 'trasformazione'
  AND (genere IS NULL OR genere NOT IN ('Totale'))
  AND indicatore IN ('Numero rapporti di lavoro', 'Numero di rapporti di lavoro', 'Valori assoluti')
GROUP BY 1, 2, 3, 4
HAVING SUM(valore) > 0
