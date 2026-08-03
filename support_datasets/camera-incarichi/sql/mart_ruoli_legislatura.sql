-- mart_ruoli_legislatura — Incarichi nei gruppi per legislatura
--
-- 1 riga = 1 legislatura: numero incarichi, gruppi distinti, deputati distinti.
-- Risponde: come si distribuiscono gli incarichi nei gruppi nel tempo?
-- Quali legislature hanno più turnover di ruoli?
--
-- PK: (legislatura)

SELECT
    legislatura,
    count(*)                                 AS n_incarichi,
    count(DISTINCT gruppo)                   AS n_gruppi,
    count(DISTINCT deputato)                 AS n_deputati
FROM clean_input
WHERE legislatura IS NOT NULL
GROUP BY legislatura
ORDER BY legislatura
