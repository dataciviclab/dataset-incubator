-- Trend annuale: bandi, importi, vincitori per anno e settore
-- Grana: 1 riga per CIG. COUNT(*) = n_CIG, non n_operatori.
SELECT
    anno,
    oggetto_principale AS settore,
    count(*) AS n_cig,
    count(DISTINCT cig) AS n_cig_distinti,
    count(DISTINCT amministrazione) AS n_sa,
    count(DISTINCT operatore) AS n_operatori,
    round(avg(importo_agg), 0) AS importo_medio,
    round(sum(importo_agg), 0) AS importo_totale,
    sum(CASE WHEN flag_pnrr THEN 1 ELSE 0 END) AS n_pnrr,
    count(*) FILTER (WHERE esito_collaudo IS NOT NULL) AS n_collaudati,
    count(*) FILTER (WHERE esito_collaudo = 'POSITIVO') AS n_collaudi_positivi
FROM clean_input
WHERE anno IS NOT NULL
GROUP BY anno, oggetto_principale
ORDER BY anno DESC, n_cig DESC
