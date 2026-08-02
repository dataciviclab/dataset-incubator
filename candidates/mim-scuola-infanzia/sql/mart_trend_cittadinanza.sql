-- mart_trend_cittadinanza — Bambini infanzia per cittadinanza × anno
--
-- 1 riga = 1 anno_scolastico: bambini italiani, non italiani, totale,
-- quota stranieri % e delta vs anno precedente. Serie temporale multi-year.
-- Serve per: bambini per cittadinanza (mappa #164), evoluzione 2018-2025.
--
-- PK: (anno_scolastico)

WITH base AS (
    SELECT
        anno_scolastico,
        SUM(bambini_italiani) AS italiani,
        SUM(bambini_non_italiani) AS non_italiani,
        SUM(bambini_totale) AS totale
    FROM clean_input
    WHERE bambini_totale IS NOT NULL
    GROUP BY anno_scolastico
),
con_lag AS (
    SELECT
        anno_scolastico,
        italiani,
        non_italiani,
        totale,
        LAG(totale) OVER (ORDER BY anno_scolastico) AS totale_anno_precedente
    FROM base
)
SELECT
    anno_scolastico,
    italiani,
    non_italiani,
    totale,
    ROUND(100.0 * non_italiani / NULLIF(totale, 0), 2) AS quota_non_italiani_pct,
    totale - totale_anno_precedente AS delta_totale,
    ROUND(100.0 * (totale - totale_anno_precedente) / NULLIF(totale_anno_precedente, 0), 1) AS variazione_pct
FROM con_lag
ORDER BY anno_scolastico
