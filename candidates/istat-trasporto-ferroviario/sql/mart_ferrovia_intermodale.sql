-- mart_ferrovia_intermodale.sql: quanto del trasporto ferroviario merci e'
-- intermodale. `TOT_INTERMODAL` e' il subtotale delle unita di carico pubblicato
-- dalla fonte: usarlo come numeratore evita di sommare le singole tipologie
-- (containers, semi-rimorchi) che sono sottoinsiemi tra loro non disgiunti.
select
    anno,
    sum(case when unita_carico = 'TOT_INTERMODAL' then valore else 0 end) as tkm_intermodale,
    sum(case when unita_carico = 'ALL' then valore else 0 end)            as tkm_totali,
    round(100.0 * sum(case when unita_carico = 'TOT_INTERMODAL' then valore else 0 end)
          / nullif(sum(case when unita_carico = 'ALL' then valore else 0 end), 0), 2) as quota_intermodale_pct
from clean_input
where unita = 'GC_TKM'
group by anno
order by anno
