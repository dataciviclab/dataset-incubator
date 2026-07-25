-- SAL: ritardi e importi per anno
SELECT
    EXTRACT(YEAR FROM data_emissione_sal) AS anno,
    flag_ritardo,
    COUNT(*) AS n_sal,
    COUNT(DISTINCT cig) AS n_cig,
    ROUND(SUM(importo_sal), 0) AS importo_totale,
    ROUND(AVG(n_giorni_scostamento), 0) AS scostamento_medio_giorni
FROM clean_input
WHERE data_emissione_sal IS NOT NULL
GROUP BY anno, flag_ritardo
ORDER BY anno DESC, n_sal DESC
