-- mart_top_beneficiari — Beneficiari con più grant e importi contrattati
--
-- 1 riga = 1 (anno, beneficiario): n grant, importo contrattato totale,
-- medio. Risponde: chi sono i giganti dei grant? (CNR, Polimi, Leonardo)
-- (D4, D7 discussion #395)
--
-- PK: (anno, beneficiario_nome)

SELECT
    anno,
    beneficiario_nome,
    count(*)                                                       AS n_grant,
    round(sum(importo_contrattato) FILTER (WHERE importo_contrattato IS NOT NULL), 0) AS importo_contrattato_totale,
    round(avg(importo_contrattato) FILTER (WHERE importo_contrattato IS NOT NULL), 0) AS importo_medio
FROM clean_input
WHERE beneficiario_nome IS NOT NULL
  AND is_rrf = 'NO'
GROUP BY anno, beneficiario_nome
ORDER BY anno, importo_contrattato_totale DESC NULLS LAST
