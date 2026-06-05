-- mart_regioni_v2.sql - mortalita_istat_evitabile
-- Output: una riga per territorio regionale (21 righe attese)
--
-- Metodologia v2: Euro-2013 proxy (Eurostat Avoidable Mortality framework)
-- Riferimento: Eurostat 2019 — lista cause amenable e preventive per eta 30-74.
-- Il perimetro qui e` esteso a 30+ (non 30-74) per coerenza con le fonti Ministero.

WITH base AS (
    SELECT
        anno,
        cod_territorio,
        territorio,
        decessi,
        pop_media
    FROM clean_input
    WHERE cod_sesso = 3
      AND cod_classe_eta = 9
      AND cod_titolo_studio = 9
      AND cod_causa IN (2, 5, 6, 7, 9, 15, 16, 17, 19, 20, 22, 24)
)
SELECT
    anno,
    cod_territorio,
    territorio,
    SUM(decessi) AS decessi_evitabili_30plus,
    MAX(pop_media) AS pop_media_30plus,
    ROUND(SUM(decessi) / NULLIF(MAX(pop_media), 0) * 10000, 2) AS tasso_grezzo_evitabile_10000_30plus
FROM base
GROUP BY anno, cod_territorio, territorio
ORDER BY cod_territorio
