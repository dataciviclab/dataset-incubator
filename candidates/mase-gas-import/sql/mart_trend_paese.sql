-- Trend per paese di origine, 1990 → ultimo anno disponibile.
-- Una riga per paese con: primo/ultimo anno **con import > 0**, valori, delta
-- assoluto e %, CAGR, picco e minimo con il relativo anno.
-- Serve per leggere il crollo della Russia e l'ascesa di Azerbaigian/GNL.
--
-- `anno_primo` è il primo anno in cui il paese compare con import > 0 (non il
-- primo anno in cui appare nella fonte): altrimenti per i fornitori nati dopo
-- il 1990 `delta_pct` e `cagr` sarebbero NULL perché la base è 0.
--
-- PK: (paese_origine)

WITH annuale AS (
    SELECT
        anno,
        paese_origine,
        SUM(import_msmc) AS import_msmc
    FROM clean_input
    GROUP BY anno, paese_origine
),
attivi AS (
    SELECT * FROM annuale WHERE import_msmc > 0
),
finestre AS (
    SELECT
        anno,
        paese_origine,
        import_msmc,
        MIN(anno) OVER (PARTITION BY paese_origine) AS anno_primo,
        MAX(anno) OVER (PARTITION BY paese_origine) AS anno_ultimo
    FROM attivi
)
SELECT
    paese_origine,
    MIN(anno_primo) AS anno_primo,
    MAX(anno_ultimo) AS anno_ultimo,
    COUNT(*) AS n_anni_attivo,
    ROUND(SUM(CASE WHEN anno = anno_primo THEN import_msmc END), 1) AS import_primo,
    ROUND(SUM(CASE WHEN anno = anno_ultimo THEN import_msmc END), 1) AS import_ultimo,
    ROUND(
        SUM(CASE WHEN anno = anno_ultimo THEN import_msmc END)
        - SUM(CASE WHEN anno = anno_primo THEN import_msmc END),
        1
    ) AS delta_assoluto,
    ROUND(
        100.0 * (
            SUM(CASE WHEN anno = anno_ultimo THEN import_msmc END)
            - SUM(CASE WHEN anno = anno_primo THEN import_msmc END)
        ) / NULLIF(SUM(CASE WHEN anno = anno_primo THEN import_msmc END), 0),
        1
    ) AS delta_pct,
    ROUND(
        POWER(
            SUM(CASE WHEN anno = anno_ultimo THEN import_msmc END)
            / NULLIF(SUM(CASE WHEN anno = anno_primo THEN import_msmc END), 0),
            1.0 / NULLIF(MAX(anno_ultimo) - MIN(anno_primo), 0)
        ) - 1,
        4
    ) AS cagr,
    ROUND(MAX(import_msmc), 1) AS import_picco,
    arg_max(anno, import_msmc) AS anno_picco,
    ROUND(MIN(import_msmc), 1) AS import_minimo,
    arg_min(anno, import_msmc) AS anno_minimo
FROM finestre
GROUP BY paese_origine
