-- mart_firmatari_ddl — numero di firmatari/presentatori per ddl
--
-- 1 riga = 1 ddl: quanti presentatori dichiarati.
-- Risponde (issue #781): quali ddl hanno più firmatari? Da quali senatori?
--
-- PK: (ddl_id)

SELECT
    ddl_id,
    count(*)                                 AS n_firmatari,
    count(*) FILTER (WHERE primo_firmatario) AS n_primi_firmatari,
    count(DISTINCT presentatore)             AS n_presentatori_distinti
FROM clean_input
GROUP BY ddl_id
ORDER BY n_firmatari DESC
