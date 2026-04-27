-- Mart: camera_deputati_legislature
-- aggregato finale dei deputati

SELECT
  deputato,
  cogn,
  nome,
  legislatura,
  gender
FROM clean_input
WHERE deputato IS NOT NULL
ORDER BY cogn, nome
;