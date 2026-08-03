-- mart_legislatura_genere — Composizione Camera per legislatura e genere
--
-- 1 riga = 1 legislatura: deputati totali, donne, quota donne %.
-- Risponde: come cambia la presenza femminile alla Camera nel tempo?
--
-- PK: (legislatura)

SELECT
    legislatura,
    count(*)                                 AS n_deputati,
    count(*) FILTER (WHERE gender = 'female') AS n_donne,
    round(100.0 * count(*) FILTER (WHERE gender = 'female') / NULLIF(count(*), 0), 1) AS quota_donne_pct
FROM clean_input
WHERE legislatura IS NOT NULL
GROUP BY legislatura
ORDER BY legislatura
