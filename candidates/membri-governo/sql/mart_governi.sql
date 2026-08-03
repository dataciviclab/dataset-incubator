-- mart_governi — Composizione per governo
--
-- 1 riga = 1 governo: membri, membri distinti, durata (da start_date min/max).
-- Risponde: quali governi hanno avuto più membri? Per ricostruire la serie
-- storica dei governi italiani (issue #786).
--
-- PK: (governo)

SELECT
    governo,
    count(*)                                 AS n_membri,
    count(DISTINCT persona_id)               AS n_persone,
    min(start_date)                          AS data_inizio,
    max(start_date)                          AS data_fine
FROM clean_input
WHERE governo IS NOT NULL
GROUP BY governo
ORDER BY n_membri DESC
