-- clean.sql — normalizza EAV indicatori + join anagrafica enti + descrizione indicatori
-- Input: raw_input.csv (da preprocess.py)
--   username;anno;ambito;indicatore;valore
-- Output: clean con denominazione, provincia, regione, descrizione_indicatore

with parsed as (
  select
    trim(cast("username" as varchar)) as username,
    try_cast(trim(cast("anno" as varchar)) as integer) as anno,
    trim(cast("ambito" as varchar)) as ambito,
    trim(cast("indicatore" as varchar)) as indicatore,
    try_cast(replace(trim(cast("valore" as varchar)), ',', '.') as double) as valore_num
  from raw_input
  where trim(coalesce(cast("username" as varchar), '')) <> ''
    and trim(coalesce(cast("indicatore" as varchar), '')) <> ''
),
enti as (
  select *
  from read_parquet('{support.opencivitas_fsc_enti_rso.mart}')
),
metadati as (
  select codice_indicatore, descrizione, tipo, categoria, funzione, anno, ambito
  from read_parquet('{root}/data/mart/opencivitas_glossario/{year}/mart_metadati.parquet')
)
select
  p.username,
  p.anno,
  p.ambito,
  p.indicatore,
  p.valore_num,
  m.descrizione as descrizione_indicatore,
  m.tipo as tipo_indicatore,
  m.categoria as categoria_indicatore,
  m.funzione as funzione_indicatore,
  e.denominazione,
  e.provincia,
  e.regione,
  e.regione_istat_cod,
  e.denominazione is not null as join_enti_ok,
  m.descrizione is not null as join_metadati_ok
from parsed p
left join enti e on p.username = e.username
left join metadati m on p.indicatore = m.codice_indicatore
                     and p.ambito = m.ambito
                     and p.anno = m.anno
where p.anno is not null
  and p.valore_num is not null
order by p.anno, p.ambito, e.regione, e.provincia, e.denominazione, p.indicatore
