-- mart_trend_mensile — Totale trasferimenti per anno × mese
--
-- 1 riga = 1 anno × mese: totale nazionale trasferimenti di residenza
-- e quota % sul totale annuo. Serve per: stagionalità della mobilità (D5),
-- effetto 2026 anno parziale (D7).
--
-- PK: (anno, mese)

WITH mensile AS (
    SELECT
        anno,
        mese,
        SUM(totale) AS trasferimenti
    FROM clean_input
    WHERE totale IS NOT NULL AND mese IS NOT NULL
    GROUP BY anno, mese
),
annuo AS (
    SELECT anno, SUM(trasferimenti) AS totale_anno
    FROM mensile
    GROUP BY anno
)
SELECT
    m.anno,
    m.mese,
    m.trasferimenti,
    ROUND(100.0 * m.trasferimenti / NULLIF(a.totale_anno, 0), 1) AS quota_mensile_pct
FROM mensile m
JOIN annuo a USING (anno)
ORDER BY m.anno, m.mese
