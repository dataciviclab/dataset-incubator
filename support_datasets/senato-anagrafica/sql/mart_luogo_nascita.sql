-- mart_luogo_nascita — senatori per luogo di nascita
--
-- 1 riga = 1 città: quanti senatori nati lì.
-- Risponde: da quali città arrivano i senatori della XIX legislatura?
--
-- PK: (luogo_nascita)

SELECT
    luogo_nascita,
    count(*) AS n_senatori
FROM clean_input
WHERE luogo_nascita IS NOT NULL
GROUP BY luogo_nascita
ORDER BY n_senatori DESC
