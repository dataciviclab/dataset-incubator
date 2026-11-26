-- mart_ferrovia_intermodale.sql: quanto del trasporto ferroviario merci e'
-- intermodale.
--
-- ATTENZIONE alle dimensioni: la fonte pubblica subtotali su piu' assi
-- (merceologia, paese di origine/destinazione, categoria di trasporto).
-- Sommare senza filtrare duplica le righe (2024: 137,8 M tkm contro i 48,3 M
-- della riga ALL/WORLD/WORLD/ALL). Si tengono solo i totali:
-- merce_nst=ALL, paese_*=WORLD, categoria_trasporto=ALL.
--
-- `TOT_INTERMODAL` e' il subtotale pubblicato delle unita di carico: usarlo
-- come numeratore evita di sommare le singole tipologie. Esiste dal 2009:
-- per 2004-2008 la quota e' NULL (nessun dato intermodale pubblicato).
select
    anno,
    sum(case when unita_carico = 'TOT_INTERMODAL' then valore end) as tkm_intermodale,
    sum(case when unita_carico = 'ALL' then valore end)            as tkm_totali,
    round(100.0 * sum(case when unita_carico = 'TOT_INTERMODAL' then valore end)
          / nullif(sum(case when unita_carico = 'ALL' then valore end), 0), 2) as quota_intermodale_pct
from clean_input
where unita = 'GC_TKM'
  and merce_nst = 'ALL'
  and paese_origine = 'WORLD'
  and paese_destinazione = 'WORLD'
  and categoria_trasporto = 'ALL'
group by anno
order by anno
