-- mart_regioni_v3.sql - mortalita_istat_evitabile
-- Baseline raccomandata: broad age-standardization 30+ su 3 bande età.
-- Output: una riga per territorio regionale (21 righe attese)

WITH base AS (
    SELECT
        anno,
        cod_territorio,
        territorio,
        cod_classe_eta,
        SUM(decessi) AS decessi_evitabili,
        MAX(pop_media) AS pop_media
    FROM clean_input
    WHERE cod_sesso = 3
      AND cod_titolo_studio = 9
      AND cod_classe_eta IN (1, 2, 3)
      AND cod_causa IN (2, 5, 6, 7, 9, 15, 16, 17, 19, 20, 22, 24)
    GROUP BY anno, cod_territorio, territorio, cod_classe_eta
),
pivoted AS (
    SELECT
        anno,
        cod_territorio,
        territorio,
        MAX(CASE WHEN cod_classe_eta = 1 THEN decessi_evitabili END) AS decessi_30_69,
        MAX(CASE WHEN cod_classe_eta = 2 THEN decessi_evitabili END) AS decessi_70_84,
        MAX(CASE WHEN cod_classe_eta = 3 THEN decessi_evitabili END) AS decessi_85_plus,
        MAX(CASE WHEN cod_classe_eta = 1 THEN pop_media END) AS pop_30_69,
        MAX(CASE WHEN cod_classe_eta = 2 THEN pop_media END) AS pop_70_84,
        MAX(CASE WHEN cod_classe_eta = 3 THEN pop_media END) AS pop_85_plus
    FROM base
    GROUP BY anno, cod_territorio, territorio
)
SELECT
    anno,
    cod_territorio,
    territorio,
    decessi_30_69 + decessi_70_84 + decessi_85_plus AS decessi_evitabili_30plus,
    pop_30_69 + pop_70_84 + pop_85_plus AS pop_media_30plus,
    ROUND(
        (decessi_30_69 + decessi_70_84 + decessi_85_plus)
        / NULLIF(pop_30_69 + pop_70_84 + pop_85_plus, 0) * 10000,
        2
    ) AS tasso_grezzo_evitabile_10000_30plus,
    ROUND(
        (
            (decessi_30_69 * 10000.0 / NULLIF(pop_30_69, 0)) * 52500 +
            (decessi_70_84 * 10000.0 / NULLIF(pop_70_84, 0)) * 11500 +
            (decessi_85_plus * 10000.0 / NULLIF(pop_85_plus, 0)) * 2500
        ) / 66500,
        2
    ) AS tasso_std_broad_evitabile_10000_30plus
FROM pivoted
ORDER BY cod_territorio
