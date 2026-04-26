with base as (
  select
    esercizio_finanziario as anno,
    codice_titolo,
    titolo,
    codice_natura,
    natura,
    sum(previsioni_definitive_cp) as totale_cp,
    sum(previsioni_definitive_cs) as totale_cs
  from clean_input
  where esercizio_finanziario between 2008 and 2024
    and codice_titolo is not null
    and codice_natura is not null
    and codice_tipologia is not null
  group by 1, 2, 3, 4, 5
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
  b.codice_titolo,
  b.titolo,
  regexp_replace(b.titolo, '^TITOLO [IVXLC]+ - ', '') as titolo_breve,
  b.codice_natura,
  b.natura,
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
order by anno, try_cast(b.codice_titolo as integer), try_cast(b.codice_natura as integer)