-- Import mensile per paese di origine + quota % sul mese.
-- Anno-mese x paese. Il totale mensile è la somma dei paesi (la riga
-- "Totale complessivo" del foglio è esclusa nel clean).

SELECT
    anno,
    mese,
    paese_origine,
    import_msmc,
    CASE
        WHEN SUM(import_msmc) OVER (PARTITION BY anno, mese) > 0
        THEN 100.0 * import_msmc / SUM(import_msmc) OVER (PARTITION BY anno, mese)
        ELSE NULL
    END AS quota_pct
FROM clean_input
