-- mart_sintesi_programma — Finanziamenti per programma e anno
--
-- 1 riga = 1 (anno, programma): grant, importo contrattato totale, medio.
-- Risponde: Horizon Europe domina? CEF Transport è il programma delle grandi
-- infrastrutture? (D2, D8, D11, D13 discussion #395)
--
-- PK: (anno, nome_programma)

SELECT
    anno,
    nome_programma,
    count(*)                                                       AS n_grant,
    round(sum(importo_contrattato) FILTER (WHERE importo_contrattato IS NOT NULL), 0) AS importo_contrattato_totale,
    round(avg(importo_contrattato) FILTER (WHERE importo_contrattato IS NOT NULL), 0) AS importo_medio,
    count(DISTINCT beneficiario_nome)                              AS n_beneficiari_distinti
FROM clean_input
WHERE nome_programma IS NOT NULL
  AND is_rrf = 'NO'
GROUP BY anno, nome_programma
ORDER BY anno, importo_contrattato_totale DESC NULLS LAST
