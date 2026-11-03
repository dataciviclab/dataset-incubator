-- Trend del consumo di gas per regione, 2004 → ultimo anno.
-- Una riga per regione con delta assoluto e %, CAGR, picco e minimo (con anno).
--
-- PK: (regione)

WITH annuale AS (
    SELECT
        anno,
        regione,
        SUM(consumo_msmc) AS consumo_msmc
    FROM clean_input
    GROUP BY anno, regione
),
finestre AS (
    SELECT
        anno,
        regione,
        consumo_msmc,
        MIN(anno) OVER (PARTITION BY regione) AS anno_primo,
        MAX(anno) OVER (PARTITION BY regione) AS anno_ultimo
    FROM annuale
)
SELECT
    regione,
    MIN(anno_primo) AS anno_primo,
    MAX(anno_ultimo) AS anno_ultimo,
    ROUND(SUM(CASE WHEN anno = anno_primo THEN consumo_msmc END), 1) AS consumo_primo,
    ROUND(SUM(CASE WHEN anno = anno_ultimo THEN consumo_msmc END), 1) AS consumo_ultimo,
    ROUND(
        SUM(CASE WHEN anno = anno_ultimo THEN consumo_msmc END)
        - SUM(CASE WHEN anno = anno_primo THEN consumo_msmc END),
        1
    ) AS delta_assoluto,
    ROUND(
        100.0 * (
            SUM(CASE WHEN anno = anno_ultimo THEN consumo_msmc END)
            - SUM(CASE WHEN anno = anno_primo THEN consumo_msmc END)
        ) / NULLIF(SUM(CASE WHEN anno = anno_primo THEN consumo_msmc END), 0),
        1
    ) AS delta_pct,
    ROUND(
        POWER(
            SUM(CASE WHEN anno = anno_ultimo THEN consumo_msmc END)
            / NULLIF(SUM(CASE WHEN anno = anno_primo THEN consumo_msmc END), 0),
            1.0 / NULLIF(MAX(anno_ultimo) - MIN(anno_primo), 0)
        ) - 1,
        4
    ) AS cagr,
    ROUND(MAX(consumo_msmc), 1) AS consumo_picco,
    arg_max(anno, consumo_msmc) AS anno_picco,
    ROUND(MIN(consumo_msmc), 1) AS consumo_minimo,
    arg_min(anno, consumo_msmc) AS anno_minimo
FROM finestre
GROUP BY regione
