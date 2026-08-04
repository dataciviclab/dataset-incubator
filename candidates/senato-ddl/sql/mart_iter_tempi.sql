-- mart_iter_tempi — Tempi dell'iter per i ddl diventati legge
--
-- 1 riga = 1 ddl approvato (con data_legge reale): giorni dall prima
-- presentazione alla legge, numero di versioni dell'atto (ping-pong
-- tra rami), ramo di partenza.
-- Risponde: quanto ci mette una legge a nascere in Italia?
-- (issue #781 — "come nasce e muore una legge")
--
-- Nota: esclude il placeholder '2100-01-01' (data fittizia del Senato
-- per 'legge pubblicata' senza data nota). Aggrega per id_ddl perché
-- il clean ha una riga per versione dell'atto.
--
-- PK: (id_ddl)

WITH per_ddl AS (
    SELECT
        id_ddl,
        max(titolo)                                                    AS titolo,
        min(data_presentazione)                                        AS data_presentazione,
        max(data_legge)                                                AS data_legge,
        count(*)                                                       AS n_versioni,
        max(progressivo_iter)                                          AS progressivo_iter,
        max(ramo)                                                      AS ramo
    FROM clean_input
    WHERE data_legge IS NOT NULL
      AND data_legge != '2100-01-01'
    GROUP BY id_ddl
)
SELECT
    id_ddl,
    titolo,
    ramo,
    n_versioni,
    data_presentazione,
    data_legge,
    date_diff('day', data_presentazione, data_legge)                   AS giorni_iter,
    round(date_diff('day', data_presentazione, data_legge) / 30.44, 1) AS mesi_iter
FROM per_ddl
ORDER BY giorni_iter DESC
