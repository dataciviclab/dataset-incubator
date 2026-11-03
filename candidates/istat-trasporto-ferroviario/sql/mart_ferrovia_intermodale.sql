-- mart_ferrovia_intermodale.sql: merci ferroviarie per unita di carico intermodale.
select
    anno,
    unita_carico,
    sum(valore) as tonnellate_km
from clean_input
where unita = 'GC_TKM'
  and unita_carico is not null
  and unita_carico <> 'ALL'
group by 1, 2
order by anno, tonnellate_km desc
