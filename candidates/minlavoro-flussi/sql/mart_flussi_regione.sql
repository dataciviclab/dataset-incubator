-- MinLavoro flussi — MART: flussi per regione × anno.
-- Fonte: RA tabelle 05.01 (attivazioni) e 05.05 (cessazioni) — geo regionale pulita.
-- Copertura 2021-2023 (RA). SUM su settore/motivo perché le tabelle sono multi-dim.

SELECT
    anno,
    'regione' AS geo_level,
    geo AS territorio,
    tipo_flusso,
    SUM(valore) AS n_rapporti
FROM clean_input
WHERE tabella_id IN ('ra_05.01', 'ra_05.05')
  AND indicatore = 'Numero rapporti di lavoro'
  AND geo IS NOT NULL
GROUP BY 1, 2, 3, 4
HAVING SUM(valore) > 0
