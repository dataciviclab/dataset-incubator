-- Collaudo: esiti per anno e tipo
SELECT
    EXTRACT(YEAR FROM data_delibera) AS anno,
    esito_collaudo,
    COUNT(*) AS n_collaudi,
    COUNT(DISTINCT cig) AS n_cig,
    ROUND(AVG(riserve_avanzate), 0) AS riserve_medie,
    ROUND(AVG(importo_contenz_risolto), 0) AS contenzioso_medio
FROM clean_input
WHERE data_delibera IS NOT NULL
GROUP BY anno, esito_collaudo
ORDER BY anno DESC, n_collaudi DESC
