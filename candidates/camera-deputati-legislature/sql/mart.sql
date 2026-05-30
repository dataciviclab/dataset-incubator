-- Mart: camera_deputati_legislature
-- aggregato finale dei deputati

SELECT
  deputato,
  cognome,
  nome,
  legislatura,
  gender
FROM clean_input
WHERE deputato IS NOT NULL
ORDER BY cognome, nome
;