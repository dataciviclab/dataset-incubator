-- mart_anno — DDL per anno di presentazione
--
-- 1 riga = 1 anno: numero ddl presentati. Risponde: la produzione
-- legislativa cresce o cala nel tempo? (issue #781)
--
-- PK: (anno)

SELECT
    EXTRACT(YEAR FROM data_presentazione)      AS anno,
    count(*)                                   AS n_ddl
FROM clean_input
WHERE data_presentazione IS NOT NULL
GROUP BY 1
ORDER BY anno
