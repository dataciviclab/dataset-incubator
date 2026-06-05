-- mart_regioni_v1.sql - mortalita_istat_evitabile
-- Baseline storica v1: mortalita totale 30+ (cod_causa=25)
-- Output: una riga per territorio regionale (21 righe attese)

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
      AND cod_causa = 25
)
SELECT
    anno,
    cod_territorio,
    territorio,
    SUM(decessi) AS decessi_30plus,
    MAX(pop_media) AS pop_media_30plus,
    ROUND(SUM(decessi) / NULLIF(MAX(pop_media), 0) * 10000, 2) AS tasso_grezzo_10000_30plus
FROM base
GROUP BY anno, cod_territorio, territorio
ORDER BY cod_territorio
