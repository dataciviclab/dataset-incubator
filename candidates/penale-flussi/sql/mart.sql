-- Mart penale_flussi: aggregazione per distretto, anno e tipo ufficio

SELECT
    anno,
    tipo_ufficio,
    distretto,
    COUNT(*) AS n_combinazioni,
    SUM(iscritti) AS tot_iscritti,
    SUM(definiti_totale) AS tot_definiti,
    SUM(pendenti_finali) AS tot_pendenti
FROM clean_input
GROUP BY anno, tipo_ufficio, distretto
ORDER BY anno, distretto, tipo_ufficio
