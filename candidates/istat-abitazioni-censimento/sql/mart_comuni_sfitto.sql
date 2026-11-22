-- mart_comuni_sfitto: stock abitativo per comune (2021, enumerazione completa)
-- Risponde a: quante abitazioni esistono, quante sono occupate, quante no.
-- Tasso di sfitto = non occupate / totale. Calcolabile solo sul 2021: nel 2019
-- (campione) manca il totale abitazioni a livello comunale.
select
    territorio_codice as codice_istat_comune,
    territorio as comune,
    anno,
    cast(round(max(case when misura_codice = 'NUM_DW_AV' then valore end)) as bigint) as abitazioni,
    cast(round(max(case when misura_codice = 'NUM_OCC_DW_AV' then valore end)) as bigint) as abitazioni_occupate,
    cast(round(max(case when misura_codice = 'NUM_UNOCC_DW_AV' then valore end)) as bigint) as abitazioni_non_occupate,
    round(
        100.0 * max(case when misura_codice = 'NUM_UNOCC_DW_AV' then valore end)
        / nullif(max(case when misura_codice = 'NUM_DW_AV' then valore end), 0),
        2
    ) as tasso_sfitto_pct
from clean_input
where livello_geografico = 'comune'
  and titolo_possesso_codice = 'ALL'
  and stanze_codice = 'TOT'
  and superficie_codice = 'ALL'
  and accessibilita_codice = 'TOTAL'
  and tipo_edificio_codice = 'TOTAL'
group by 1, 2, 3
-- solo le edizioni con il totale dello stock (2021): nel 2019 il censimento
-- campionario non espone NUM_DW_AV a livello comunale, quindi il tasso non esiste
having max(case when misura_codice = 'NUM_DW_AV' then 1 else 0 end) = 1
order by tasso_sfitto_pct desc
