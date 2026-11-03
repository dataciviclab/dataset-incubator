-- Import per paese, alla granularità nativa della fonte:
-- mensile 2002-2024, annuale 1990-2001.
-- `quota_periodo_pct` è la quota sul totale del **periodo nativo**: anno-mese per
-- le righe mensili, anno per quelle annuali. Il nome lo dice perché la colonna
-- cambia significato con `granularita`.

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
    END AS quota_periodo_pct
FROM clean_input
