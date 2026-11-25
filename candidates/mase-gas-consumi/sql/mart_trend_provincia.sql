-- Trend del consumo di gas per provincia, 2004 → ultimo anno.
-- Una riga per provincia con regione, delta assoluto e %, CAGR, picco e minimo.
-- Serve per leggere chi cresce e chi esce dal gas (es. province industriali).
--
-- PK: (provincia)

WITH annuale AS (
    SELECT
        anno,
        regione,
        provincia,
        SUM(consumo_msmc) AS consumo_msmc
    FROM clean_input
    GROUP BY anno, regione, provincia
),
finestre AS (
    SELECT
        anno,
        regione,
        provincia,
        consumo_msmc,
        MIN(anno) OVER (PARTITION BY provincia) AS anno_primo,
        MAX(anno) OVER (PARTITION BY provincia) AS anno_ultimo
    FROM annuale
)
SELECT
    provincia,
    MAX(regione) AS regione,
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
    arg_max(anno, consumo_msmc) AS anno_picco
FROM finestre
GROUP BY provincia
