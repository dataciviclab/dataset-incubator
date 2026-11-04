-- Trend dei consumi petroliferi per prodotto, 2002 → ultimo anno.
-- Una riga per prodotto con delta assoluto e %, CAGR, picco e minimo (con anno).
-- Esclude la riga di sintesi `totale prodotti principali` (non è un prodotto).
--
-- PK: (prodotto)

WITH annuale AS (
    SELECT
        anno,
        prodotto,
        SUM(consumo_kt) AS consumo_kt
    FROM clean_input
    WHERE prodotto <> 'totale prodotti principali'
    GROUP BY anno, prodotto
),
finestre AS (
    SELECT
        anno,
        prodotto,
        consumo_kt,
        MIN(anno) OVER (PARTITION BY prodotto) AS anno_primo,
        MAX(anno) OVER (PARTITION BY prodotto) AS anno_ultimo
    FROM annuale
)
SELECT
    prodotto,
    MIN(anno_primo) AS anno_primo,
    MAX(anno_ultimo) AS anno_ultimo,
    ROUND(SUM(CASE WHEN anno = anno_primo THEN consumo_kt END), 1) AS consumo_primo,
    ROUND(SUM(CASE WHEN anno = anno_ultimo THEN consumo_kt END), 1) AS consumo_ultimo,
    ROUND(
        SUM(CASE WHEN anno = anno_ultimo THEN consumo_kt END)
        - SUM(CASE WHEN anno = anno_primo THEN consumo_kt END),
        1
    ) AS delta_assoluto,
    ROUND(
        100.0 * (
            SUM(CASE WHEN anno = anno_ultimo THEN consumo_kt END)
            - SUM(CASE WHEN anno = anno_primo THEN consumo_kt END)
        ) / NULLIF(SUM(CASE WHEN anno = anno_primo THEN consumo_kt END), 0),
        1
    ) AS delta_pct,
    ROUND(
        POWER(
            SUM(CASE WHEN anno = anno_ultimo THEN consumo_kt END)
            / NULLIF(SUM(CASE WHEN anno = anno_primo THEN consumo_kt END), 0),
            1.0 / NULLIF(MAX(anno_ultimo) - MIN(anno_primo), 0)
        ) - 1,
        4
    ) AS cagr,
    ROUND(MAX(consumo_kt), 1) AS consumo_picco,
    arg_max(anno, consumo_kt) AS anno_picco,
    ROUND(MIN(consumo_kt), 1) AS consumo_minimo,
    arg_min(anno, consumo_kt) AS anno_minimo
FROM finestre
GROUP BY prodotto
