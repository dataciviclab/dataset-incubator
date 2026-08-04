-- mart_tipo_iniziativa — presentatori per tipo di iniziativa
--
-- 1 riga = 1 tipo (Parlamentare / Governativa / ...): numero di presentatori.
-- Risponde (issue #781): i ddl nascono da iniziativa parlamentare o governativa?
--
-- PK: (tipo_iniziativa)

SELECT
    tipo_iniziativa,
    count(*)                                 AS n_firmatari,
    count(DISTINCT ddl_id)                   AS n_ddl
FROM clean_input
WHERE tipo_iniziativa IS NOT NULL
GROUP BY tipo_iniziativa
ORDER BY n_firmatari DESC
