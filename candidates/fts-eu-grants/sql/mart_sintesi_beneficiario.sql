-- mart_sintesi_beneficiario — Finanziamenti per tipo beneficiario e anno
--
-- 1 riga = 1 (anno, tipo beneficiario): grant, importo contrattato totale,
-- medio. Risponde: imprese > PA? ONG e terzo settore quanto valgono?
-- (D3, D6 discussion #395)
--
-- PK: (anno, tipo_beneficiario)

SELECT
    anno,
    tipo_beneficiario,
    count(*)                                                       AS n_grant,
    round(sum(importo_contrattato) FILTER (WHERE importo_contrattato IS NOT NULL), 0) AS importo_contrattato_totale,
    round(avg(importo_contrattato) FILTER (WHERE importo_contrattato IS NOT NULL), 0) AS importo_medio
FROM clean_input
WHERE tipo_beneficiario IS NOT NULL
  AND is_rrf = 'NO'
GROUP BY anno, tipo_beneficiario
ORDER BY anno, importo_contrattato_totale DESC NULLS LAST
