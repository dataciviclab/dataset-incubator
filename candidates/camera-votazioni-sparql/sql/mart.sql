-- mart_votazioni_anno — serie per anno delle votazioni Camera
-- Metriche dell'analisi pubblica "Camera votazioni 2018-2025":
--   votazioni, media votanti, media favorevoli/contrari, fiducia,
--   votazioni finali approvate, voto segreto.
SELECT
    year(data)                                                              AS anno,
    count(*)                                                                AS n_votazioni,
    round(avg(votanti), 1)                                                  AS media_votanti,
    round(avg(favorevoli), 1)                                               AS media_favorevoli,
    round(avg(contrari), 1)                                                 AS media_contrari,
    round(avg(astenuti), 1)                                                 AS media_astenuti,
    round(avg(presenti), 1)                                                 AS media_presenti,
    sum(CASE WHEN richiesta_fiducia THEN 1 ELSE 0 END)                      AS n_fiducia,
    sum(CASE WHEN votazione_finale THEN 1 ELSE 0 END)                       AS n_votazioni_finali,
    sum(CASE WHEN votazione_finale AND approvato THEN 1 ELSE 0 END)         AS n_finali_approvate,
    sum(CASE WHEN votazione_segreta THEN 1 ELSE 0 END)                      AS n_segrete,
    round(
        100.0 * sum(CASE WHEN votazione_finale AND approvato THEN 1 ELSE 0 END)
        / NULLIF(sum(CASE WHEN votazione_finale THEN 1 ELSE 0 END), 0), 1
    )                                                                       AS pct_finali_approvate
FROM clean_input
GROUP BY year(data)
ORDER BY anno
