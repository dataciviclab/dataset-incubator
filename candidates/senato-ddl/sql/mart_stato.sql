-- mart_stato — DDL per stato dell'iter
--
-- 1 riga = 1 stato: numero ddl. Risponde: come si distribuisce l'iter
-- legislativo? Quanti ddl approvati vs fermi in commissione?
-- (issue #781)
--
-- PK: (stato)

SELECT
    stato,
    count(*)                                 AS n_ddl
FROM clean_input
WHERE stato IS NOT NULL
GROUP BY stato
ORDER BY n_ddl DESC
