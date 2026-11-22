-- mart_affitto_2019: abitazioni occupate per titolo di possesso, per comune e anno
-- Fonte: DF_DCSS_ABITAZIONI_TV_2. Il dettaglio per titolo di possesso esiste SOLO per il 2019
-- (2021 e 2023 espongono solo il totale ALL). Valori campionari: stime, non conteggi.
select
    territorio_codice as codice_istat_comune,
    anno,
    round(sum(case when titolo_possesso_codice = 'OWN' then valore end), 0) as occupate_proprieta,
    round(sum(case when titolo_possesso_codice = 'RENT' then valore end), 0) as occupate_affitto,
    round(sum(case when titolo_possesso_codice = 'OTH_OR' then valore end), 0) as occupate_altro,
    round(
        100.0 * sum(case when titolo_possesso_codice = 'RENT' then valore end)
        / nullif(sum(case when titolo_possesso_codice in ('OWN', 'RENT', 'OTH_OR') then valore end), 0),
        2
    ) as quota_affitto_pct,
    case when anno = 2021 then 'enumerazione' else 'campione' end as tipo_rilevazione
from clean_input
where livello_geografico = 'comune'
  and misura_codice = 'NUM_OCC_DW_AV'
  and titolo_possesso_codice in ('OWN', 'RENT', 'OTH_OR')
group by 1, 2
-- solo le edizioni con il dettaglio per titolo completo
having count(distinct titolo_possesso_codice) = 3
order by anno, quota_affitto_pct desc
