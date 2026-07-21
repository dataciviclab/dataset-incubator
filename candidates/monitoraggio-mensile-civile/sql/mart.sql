-- Mart monitoraggio_mensile_civile: trend mensili per distretto e area

SELECT
    anno,
    mese,
    area,
    distretto,
    COUNT(*) AS n_combinazioni,
    SUM(iscritti) AS tot_iscritti,
    SUM(definiti) AS tot_definiti,
    ROUND(SUM(definiti)::NUMERIC / NULLIF(SUM(iscritti), 0), 4) AS clearance_rate_mensile
FROM clean_input
GROUP BY anno, mese, area, distretto
ORDER BY anno, mese, area, distretto
