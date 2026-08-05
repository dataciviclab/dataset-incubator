SELECT
    stato_avanzamento,
    COUNT(DISTINCT cup) AS n_progetti,
    ROUND(SUM(fin_pnrr)) AS tot_fin_pnrr,
    ROUND(SUM(fin_totale)) AS tot_fin_totale,
    ROUND(SUM(fin_pnrr) / NULLIF(SUM(SUM(fin_pnrr)) OVER (), 0) * 100, 2) AS pct_fin_pnrr
FROM clean_input
GROUP BY stato_avanzamento
