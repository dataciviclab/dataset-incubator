-- mart_nascita_anno — senatori per anno di nascita
--
-- 1 riga = 1 anno: quanti senatori nati in quell'anno (distribuzione età).
-- Risponde: com'è distribuita l'età dei senatori della XIX legislatura?
--
-- PK: (anno_nascita)

SELECT
    EXTRACT(YEAR FROM data_nascita) AS anno_nascita,
    count(*)                        AS n_senatori
FROM clean_input
WHERE data_nascita IS NOT NULL
GROUP BY 1
ORDER BY anno_nascita
