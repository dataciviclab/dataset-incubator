-- mart_stato — DDL per stato dell'iter
--
-- 1 riga = 1 stato: numero di DDL DISTINTI (non righe — una riga è una
-- versione dell'atto nell'iter, un ddl può avere più versioni).
-- Risponde: come si distribuisce l'iter legislativo? Quanti ddl approvati
-- vs fermi in commissione? (issue #781)
--
-- PK: (stato)

SELECT
    stato,
    count(DISTINCT id_ddl)                   AS n_ddl
FROM clean_input
WHERE stato IS NOT NULL
GROUP BY stato
ORDER BY n_ddl DESC
