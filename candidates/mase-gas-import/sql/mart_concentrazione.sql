-- Concentrazione delle importazioni per anno: la misura della dipendenza.
-- Una riga per anno con HHI, quote top-1/3/5, numero di fornitori.
--
-- HHI = somma dei quadrati delle quote (frazioni 0-1). Soglie usuali:
--   < 0,15 concorrenziale · 0,15-0,25 moderata · > 0,25 concentrata.
--
-- `n_paesi_reali` esclude i bucket aggregati (`ALTRI UE`, `ALTRI NON UE`,
-- `NON SPECIFICATO`, `SCONOSCIUTO`): HHI e quote restano calcolati su **tutto**
-- l'import, così le quote sommano 100 e il denominatore è il totale reale.
--
-- PK: (anno)

WITH annuale AS (
    SELECT
        anno,
        paese_origine,
        SUM(import_msmc) AS import_msmc
    FROM clean_input
    GROUP BY anno, paese_origine
),
tot AS (
    SELECT anno, SUM(import_msmc) AS import_totale
    FROM annuale
    GROUP BY anno
),
classificato AS (
    SELECT
        a.anno,
        a.paese_origine,
        a.import_msmc,
        t.import_totale,
        100.0 * a.import_msmc / NULLIF(t.import_totale, 0) AS quota_pct,
        ROW_NUMBER() OVER (PARTITION BY a.anno ORDER BY a.import_msmc DESC) AS posizione,
        a.paese_origine NOT IN (
            'ALTRI UE', 'ALTRI NON UE', 'NON SPECIFICATO', 'SCONOSCIUTO'
        ) AS is_paese
    FROM annuale a
    JOIN tot t USING (anno)
)
SELECT
    anno,
    ROUND(SUM(POWER(quota_pct / 100.0, 2)), 4) AS hhi,
    ROUND(SUM(quota_pct) FILTER (WHERE posizione <= 1), 1) AS top1_pct,
    ROUND(SUM(quota_pct) FILTER (WHERE posizione <= 3), 1) AS top3_pct,
    ROUND(SUM(quota_pct) FILTER (WHERE posizione <= 5), 1) AS top5_pct,
    COUNT(*) FILTER (WHERE import_msmc > 0) AS n_fornitori_attivi,
    COUNT(*) FILTER (WHERE is_paese AND import_msmc > 0) AS n_paesi_reali,
    ROUND(MAX(import_totale), 1) AS import_totale
FROM classificato
GROUP BY anno
