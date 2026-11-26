-- mart_oneri_per_rts.sql: costo e partite per ufficio territoriale (RTS) e anno.
-- `quota_pct` e' la quota dell'importo totale dell'anno.
select
  anno,
  rts,
  descrizione_rts,
  sum(numero_partite) as numero_partite,
  sum(importi_totale_eur) as importi_totale_eur,
  round(
    100.0 * sum(importi_totale_eur)
    / nullif(sum(sum(importi_totale_eur)) over (partition by anno), 0),
    2
  ) as quota_pct
from clean_input
group by anno, rts, descrizione_rts
order by anno desc, importi_totale_eur desc
