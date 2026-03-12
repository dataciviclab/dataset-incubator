-- mart_regioni_v3.sql - malasanita_d_mortalita_istat
-- Output: una riga per territorio regionale (21 righe attese)
--
-- Metodologia v3: broad age-standardization 30+ su 3 bande età.
-- La fonte D non espone classi quinquennali sufficienti per una ESP2013 piena:
-- rende disponibili solo:
--   1 = 30-69 anni
--   2 = 70-84 anni
--   3 = 85 e più anni
--
-- Per questo la v3 usa una standardizzazione esplicita ma "a bande larghe",
-- aggregando i pesi ESP2013 sulle tre fasce disponibili:
--   30-69 -> 52.500
--   70-84 -> 11.500
--   85+   ->  2.500
--   totale 30+ -> 66.500
--
-- Validazione metodologica interna:
-- applicata al totale cause (cod_causa=25), questa broad-standardization
-- replica bene il tasso standardizzato della fonte per 30+:
-- correlazione ~0.99 sulle 21 regioni/PA.
--
-- Quindi:
-- - v2 resta il proxy grezzo 30+ sulle 12 cause Euro-2013
-- - v3 aggiunge una metrica standardizzata difendibile con i dati disponibili
-- - non sostituisce una standardizzazione piena a 5 anni, che la fonte non consente

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
