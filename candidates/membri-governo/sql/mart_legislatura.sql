-- mart_legislatura — Membri del governo per legislatura
--
-- 1 riga = 1 legislatura: membri, governi distinti.
-- Risponde: quanti membri del governo per legislatura? Serie storica
-- dal Regno alla Repubblica (issue #786).
-- Nota: il gender si ottiene con join a camera_deputati_legislature
-- per persona_id (non incluso qui — il grafo governo non espone foaf:gender).
--
-- PK: (legislatura)

SELECT
    legislatura,
    count(*)                                 AS n_membri,
    count(DISTINCT governo)                  AS n_governi
FROM clean_input
WHERE legislatura IS NOT NULL
GROUP BY legislatura
ORDER BY legislatura
