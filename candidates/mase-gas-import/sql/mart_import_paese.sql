-- Import per paese, alla granularità nativa della fonte:
-- mensile 2002-2024, annuale 1990-2001.
-- `quota_pct` è la quota sul totale del periodo (anno-mese per il mensile,
-- anno per l'annuale).

SELECT
    anno,
    mese,
    granularita,
    paese_origine,
    import_msmc,
    CASE
        WHEN SUM(import_msmc) OVER (PARTITION BY anno, mese) > 0
        THEN 100.0 * import_msmc / SUM(import_msmc) OVER (PARTITION BY anno, mese)
        ELSE NULL
    END AS quota_pct
FROM clean_input
