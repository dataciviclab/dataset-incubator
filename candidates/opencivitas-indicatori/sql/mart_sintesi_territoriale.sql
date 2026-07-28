-- mart_sintesi_territoriale.sql
-- Statistiche descrittive per livello territoriale (provincia, regione, nazionale).
-- Per ogni (livello, codice_area, anno, ambito, indicatore):
--   media, mediana, q25, q75, min, max, std, n_comuni
--
-- Input: clean_input (senza codice_istat) + comuni_master
-- La join usa denominazione + provincia (codice 3 cifre) come fa mart.sql

with
comuni as (
  select
    codice_istat,
    denominazione,
    provincia,
    substr(codice_istat, 1, 3) as prov_cod,
    regione,
    flag_capoluogo,
    ripartizione
  from read_parquet('{support.comuni_master.mart}')
),
base as (
  select
    c.anno,
    c.ambito,
    c.indicatore,
    c.valore_num,
    cm.codice_istat,
    cm.regione,
    cm.flag_capoluogo,
    cm.ripartizione
  from clean_input c
  inner join comuni cm
    on upper(cm.denominazione) = upper(c.denominazione)
    and cm.prov_cod = c.provincia
  where c.valore_num is not null
    and c.tipo_indicatore in ('IND', 'DET')
),
agg_provincia as (
  select
    'provincia' as livello_territoriale,
    substr(base.codice_istat, 1, 3) as codice_area,
    max(cm2.provincia) as nome_area,
    anno,
    ambito,
    indicatore,
    count(*) as n_comuni,
    avg(valore_num) as media,
    median(valore_num) as mediana,
    percentile_cont(0.25) within group (order by valore_num) as q25,
    percentile_cont(0.75) within group (order by valore_num) as q75,
    min(valore_num) as minimo,
    max(valore_num) as massimo,
    stddev(valore_num) as dev_std,
    avg(case when base.flag_capoluogo then valore_num end) as media_capoluoghi
  from base
  left join comuni cm2 on base.codice_istat = cm2.codice_istat
  group by substr(base.codice_istat, 1, 3), anno, ambito, indicatore
),
agg_regione as (
  select
    'regione' as livello_territoriale,
    regione as codice_area,
    regione as nome_area,
    anno,
    ambito,
    indicatore,
    count(*) as n_comuni,
    avg(valore_num) as media,
    median(valore_num) as mediana,
    percentile_cont(0.25) within group (order by valore_num) as q25,
    percentile_cont(0.75) within group (order by valore_num) as q75,
    min(valore_num) as minimo,
    max(valore_num) as massimo,
    stddev(valore_num) as dev_std,
    avg(case when flag_capoluogo then valore_num end) as media_capoluoghi
  from base
  group by regione, anno, ambito, indicatore
),
agg_nazionale as (
  select
    'nazionale' as livello_territoriale,
    'IT' as codice_area,
    'Italia' as nome_area,
    anno,
    ambito,
    indicatore,
    count(*) as n_comuni,
    avg(valore_num) as media,
    median(valore_num) as mediana,
    percentile_cont(0.25) within group (order by valore_num) as q25,
    percentile_cont(0.75) within group (order by valore_num) as q75,
    min(valore_num) as minimo,
    max(valore_num) as massimo,
    stddev(valore_num) as dev_std,
    avg(case when flag_capoluogo then valore_num end) as media_capoluoghi
  from base
  group by anno, ambito, indicatore
)
select * from agg_provincia
union all
select * from agg_regione
union all
select * from agg_nazionale
order by livello_territoriale, codice_area, anno, ambito, indicatore
