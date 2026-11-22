-- mart_affitto_2019: abitazioni occupate per titolo di possesso, per comune
-- Attenzione: 2019 e' l'edizione campionaria del censimento permanente.
-- I valori sono stime (decimali) e riguardano SOLO le abitazioni occupate:
-- non esiste il totale dello stock comunale per il 2019.
select
    territorio_codice as codice_istat_comune,
    territorio as comune,
    anno,
    round(sum(case when titolo_possesso_codice = 'OWN' then valore end), 0) as occupate_proprieta,
    round(sum(case when titolo_possesso_codice = 'RENT' then valore end), 0) as occupate_affitto,
    round(sum(case when titolo_possesso_codice = 'OTH_OR' then valore end), 0) as occupate_altro,
    round(
        100.0 * sum(case when titolo_possesso_codice = 'RENT' then valore end)
        / nullif(sum(case when titolo_possesso_codice in ('OWN', 'RENT', 'OTH_OR') then valore end), 0),
        2
    ) as quota_affitto_pct
from clean_input
where livello_geografico = 'comune'
  and misura_codice = 'NUM_OCC_DW_AV'
  and titolo_possesso_codice in ('OWN', 'RENT', 'OTH_OR')
  and stanze_codice = 'TOT'
  and superficie_codice = 'ALL'
  and accessibilita_codice = 'TOTAL'
  and tipo_edificio_codice = 'TOTAL'
group by 1, 2, 3
-- solo le edizioni con il dettaglio per titolo di possesso (2019): il 2021
-- espone le sole righe di totale (ALL) e non deve entrare in questo mart
having count(distinct titolo_possesso_codice) = 3
order by quota_affitto_pct desc
