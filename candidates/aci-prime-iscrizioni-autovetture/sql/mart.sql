SELECT
  anno,
  alimentazione,
  SUM(prime_iscrizioni) AS prime_iscrizioni
FROM clean_input
GROUP BY anno, alimentazione
ORDER BY anno, alimentazione
