with base as (
  select
    esercizio_finanziario as anno,
    missione,
    sum(previsioni_definitive_cp) as totale_cp,
    sum(previsioni_definitive_cs) as totale_cs
  from clean_input
  where esercizio_finanziario between 2008 and 2024
    and missione is not null
  group by 1, 2
),
totali_anno as (
  select
    anno,
    sum(totale_cp) as anno_totale_cp,
    sum(totale_cs) as anno_totale_cs
  from base
  group by 1
)
select
  b.anno,
  b.missione,
  b.totale_cp,
  b.totale_cs,
  case
    when t.anno_totale_cp = 0 then null
    else b.totale_cp / t.anno_totale_cp
  end as quota_cp,
  case
    when t.anno_totale_cs = 0 then null
    else b.totale_cs / t.anno_totale_cs
  end as quota_cs
from base b
join totali_anno t using (anno)
order by anno, b.missione
