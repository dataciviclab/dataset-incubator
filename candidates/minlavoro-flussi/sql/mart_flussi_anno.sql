-- MinLavoro flussi — MART: flussi nazionali per anno × genere × tipologia contratto.
-- Fonte: NOTA tabelle 03 (attivati) e 07 (cessati) — genere × tipologia, senza geo.
-- SUM su trimestre perché la NOTA pubblica valori per-trimestre.

SELECT
    anno,
    tipo_flusso,
    genere,
    tipologia_contratto,
    SUM(valore) AS n_rapporti
FROM clean_input
WHERE tabella_id IN ('nota_03', 'nota_07')
  AND genere IN ('Maschi', 'Femmine')
  AND tipologia_contratto IS NOT NULL
  AND indicatore ILIKE 'Numero di rapporti%'
GROUP BY 1, 2, 3, 4
HAVING SUM(valore) > 0
