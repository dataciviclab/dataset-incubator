-- mart_comuni_sfitto: stock abitativo per comune e anno (2019, 2021, 2023)
-- Tasso di sfitto = non occupate / totale.
-- 2021 e' enumerazione completa; 2019 e 2023 sono edizioni campionarie (stime).
select
    territorio_codice as codice_istat_comune,
    anno,
    cast(round(max(case when misura_codice = 'NUM_DW_AV' then valore end)) as bigint) as abitazioni,
    cast(round(max(case when misura_codice = 'NUM_OCC_DW_AV' then valore end)) as bigint) as abitazioni_occupate,
    cast(round(max(case when misura_codice = 'NUM_UNOCC_DW_AV' then valore end)) as bigint) as abitazioni_non_occupate,
    round(
        100.0 * max(case when misura_codice = 'NUM_UNOCC_DW_AV' then valore end)
        / nullif(max(case when misura_codice = 'NUM_DW_AV' then valore end), 0),
        2
    ) as tasso_sfitto_pct,
    max(tipo_rilevazione) as tipo_rilevazione
from clean_input
where livello_geografico = 'comune'
  and titolo_possesso_codice = 'ALL'
group by 1, 2
-- solo le edizioni con il totale dello stock: edition-proof
having max(case when misura_codice = 'NUM_DW_AV' then 1 else 0 end) = 1
order by anno, tasso_sfitto_pct desc
