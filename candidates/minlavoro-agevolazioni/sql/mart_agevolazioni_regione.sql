-- MinLavoro agevolazioni — MART: dichiarazioni per regione × anno × tipo.
-- Unisce decontribuzione e detassazione (le due serie mensili con anno).

SELECT
    regione,
    anno,
    tipo_agevolazione,
    SUM(valore) AS n_dichiarazioni
FROM clean_input
WHERE regione IS NOT NULL
  AND anno IS NOT NULL
  AND tipo_agevolazione IN ('decontribuzione', 'detassazione')
  AND (
        indicatore ILIKE '%dichiarazioni%'
     OR indicatore ILIKE '%Num%contratti%'
  )
GROUP BY 1, 2, 3
HAVING SUM(valore) > 0
