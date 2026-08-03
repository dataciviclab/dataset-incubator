-- mart_top_deputati — Deputati con più incarichi nei gruppi
--
-- 1 riga = 1 deputato: numero incarichi, gruppi distinti, ruoli distinti.
-- Risponde: chi ha ricoperto più ruoli nei gruppi parlamentari?
--
-- PK: (deputato)

SELECT
    deputato,
    count(*)                                 AS n_incarichi,
    count(DISTINCT gruppo)                   AS n_gruppi,
    count(DISTINCT ruolo)                    AS n_ruoli
FROM clean_input
WHERE deputato IS NOT NULL
GROUP BY deputato
ORDER BY n_incarichi DESC
