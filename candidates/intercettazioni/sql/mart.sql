-- Mart intercettazioni: trend per distretto e tipologia

SELECT
    anno,
    distretto,
    tipologia_intercettazione,
    SUM(n_bersagli) AS tot_bersagli,
    COUNT(*) AS n_combinazioni
FROM clean_input
GROUP BY anno, distretto, tipologia_intercettazione
ORDER BY anno, tot_bersagli DESC
