-- MinLavoro agevolazioni — MART: totali nazionali per anno × tipo.

SELECT
    anno,
    tipo_agevolazione,
    SUM(valore) AS n_dichiarazioni
FROM clean_input
WHERE anno IS NOT NULL
  AND tipo_agevolazione IN ('decontribuzione', 'detassazione')
  AND (
        indicatore ILIKE '%dichiarazioni%'
     OR indicatore ILIKE '%Num%contratti%'
  )
GROUP BY 1, 2
HAVING SUM(valore) > 0
