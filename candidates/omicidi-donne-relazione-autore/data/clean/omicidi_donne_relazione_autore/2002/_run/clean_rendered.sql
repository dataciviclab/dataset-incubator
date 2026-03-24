WITH raw_data AS (
    SELECT * FROM raw
),
filtered AS (
    -- OFFSET 6 salta le prime 6 righe di intestazione "sporca" dell'Excel
    -- LIMIT 7 prende le 7 categorie di relazione (coniuge, ex, ecc.)
    SELECT * FROM raw_data OFFSET 6 LIMIT 7
)
SELECT 
    column0 AS relazione,
    column1 AS "2002", column2 AS "2003", column3 AS "2004", column4 AS "2005",
    column5 AS "2006", column6 AS "2007", column7 AS "2008", column8 AS "2009",
    column9 AS "2010", column10 AS "2011", column11 AS "2012", column12 AS "2013",
    column13 AS "2014", column14 AS "2015", column15 AS "2016", column16 AS "2017",
    column17 AS "2018", column18 AS "2019", column19 AS "2020", column20 AS "2021",
    column21 AS "2022", column22 AS "2023", column23 AS "2024"
FROM filtered
WHERE relazione IS NOT NULL AND relazione != 'TOTALE'