-- Serie annuale per paese: il mensile è aggregato, l'annuale (1990-2001) è già tale.
-- Una riga per anno × paese, con quota % sull'anno. È la tabella per leggere
-- l'evoluzione del mix di fornitori dal 1990.

SELECT
    anno,
    paese_origine,
    SUM(import_msmc) AS import_msmc,
    CASE
        WHEN SUM(SUM(import_msmc)) OVER (PARTITION BY anno) > 0
        THEN 100.0 * SUM(import_msmc) / SUM(SUM(import_msmc)) OVER (PARTITION BY anno)
        ELSE NULL
    END AS quota_pct
FROM clean_input
GROUP BY anno, paese_origine
