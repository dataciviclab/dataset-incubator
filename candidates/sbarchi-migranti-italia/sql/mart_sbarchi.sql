SELECT
    DATE_TRUNC('month', data_sbarchi) AS mese,
    COUNT(*) AS giorni_con_sbarchi,
    SUM(valore) AS tot_sbarchi,
    AVG(valore) AS media_giornaliera,
    MAX(valore) AS picco_giornaliero,
    MIN(valore) AS minimo_giornaliero
FROM clean_input
WHERE data_sbarchi IS NOT NULL AND valore IS NOT NULL AND valore > 0
GROUP BY DATE_TRUNC('month', data_sbarchi)
ORDER BY mese
