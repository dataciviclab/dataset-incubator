-- MASE SISEN — "Importazioni di gas naturale per paese di origine".
-- File: ImportazioniGasMensiliPerPaeseDiOrigine_YYYY.xlsx, foglio "Foglio2".
-- Layout non tabellare: titolo a riga 3, nomi mesi a riga 5, paesi da riga 6.
--   read.skip=4 + header=true  ->  header = riga 5, paese in colonna 0 (rinominata "paese").
-- Il foglio "Foglio1" è un pivot ausiliario: ignorato via sheet_name.
-- Le colonne mese arrivano con tipi misti (VARCHAR/DOUBLE) -> cast esplicito prima di UNPIVOT.
-- Unità: M Sm3 (milioni di Sm3), PCS 10,57275 kWh/Sm3.
-- Esclusa la riga "Totale complessivo": il totale si ricalcola nel mart.

WITH src AS (
    SELECT
        TRIM(CAST(paese AS VARCHAR)) AS paese,
        CAST(gen AS VARCHAR) AS gen,
        CAST(feb AS VARCHAR) AS feb,
        CAST(mar AS VARCHAR) AS mar,
        CAST(apr AS VARCHAR) AS apr,
        CAST(mag AS VARCHAR) AS mag,
        CAST(giu AS VARCHAR) AS giu,
        CAST(lug AS VARCHAR) AS lug,
        CAST(ago AS VARCHAR) AS ago,
        CAST(set AS VARCHAR) AS set,
        CAST(ott AS VARCHAR) AS ott,
        CAST(nov AS VARCHAR) AS nov,
        CAST(dic AS VARCHAR) AS dic
    FROM raw_input
),
long AS (
    UNPIVOT src
    ON gen, feb, mar, apr, mag, giu, lug, ago, set, ott, nov, dic
    INTO NAME mese_nome VALUE import_msmc
)
SELECT
    {year} AS anno,
    CASE mese_nome
        WHEN 'gen' THEN 1 WHEN 'feb' THEN 2 WHEN 'mar' THEN 3 WHEN 'apr' THEN 4
        WHEN 'mag' THEN 5 WHEN 'giu' THEN 6 WHEN 'lug' THEN 7 WHEN 'ago' THEN 8
        WHEN 'set' THEN 9 WHEN 'ott' THEN 10 WHEN 'nov' THEN 11 WHEN 'dic' THEN 12
    END AS mese,
    paese AS paese_origine,
    TRY_CAST(import_msmc AS DOUBLE) AS import_msmc
FROM long
WHERE paese IS NOT NULL
  AND paese <> ''
  AND lower(paese) NOT LIKE 'totale%'
