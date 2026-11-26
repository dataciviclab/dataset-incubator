-- mart_oneri_per_ministero.sql: costo e partite per amministrazione e anno.
-- `quota_pct` e' la quota dell'importo totale dell'anno.
select
  anno,
  ministero,
  sum(numero_partite) as numero_partite,
  sum(importi_arretrati_eur) as importi_arretrati_eur,
  sum(importi_ratei_eur) as importi_ratei_eur,
  sum(importi_tredicesima_eur) as importi_tredicesima_eur,
  sum(importi_totale_eur) as importi_totale_eur,
  round(
    100.0 * sum(importi_totale_eur)
    / nullif(sum(sum(importi_totale_eur)) over (partition by anno), 0),
    2
  ) as quota_pct
from clean_input
group by anno, ministero
order by anno desc, importi_totale_eur desc
