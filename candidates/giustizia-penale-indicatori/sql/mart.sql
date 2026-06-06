-- Mart: Giustizia penale - clearance rate e disposition time per anno e distretto
SELECT
    anno,
    distretto,
    tipo_ufficio,
    COUNT(*)                           AS num_sedi,
    AVG(clearance_rate)                AS clearance_rate_medio,
    AVG(disposition_time_gg)           AS disposition_time_medio,
    MIN(clearance_rate)                AS clearance_rate_min,
    MAX(clearance_rate)                AS clearance_rate_max,
    MIN(disposition_time_gg)           AS disposition_time_min_gg,
    MAX(disposition_time_gg)           AS disposition_time_max_gg
FROM clean_input
GROUP BY anno, distretto, tipo_ufficio
ORDER BY anno, distretto;
