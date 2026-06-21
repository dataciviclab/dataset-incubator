-- clean.sql — FSC multi-anno: pivot EAV→wide + join geografico
-- Colonne raw sempre per posizione (col0=USERNAME, col1=nome, col2=valore)
-- Compatibile con tutti i formati (VAR_FSC_NAME/VAR_FSC_VAL e varianti)

with parsed as (
  select
    trim("column00") as username,
    trim("column01") as componente,
    try_cast(replace(trim(cast("column02" as varchar)), ',', '.') as double) as valore_num
  from raw_input
  where trim(coalesce("column00", '')) <> ''
    and trim(coalesce("column01", '')) <> ''
),
fsc as (
  select
    username,
    max(case when componente = 'POPOLAZIONE' then valore_num end) as popolazione,
    max(case when componente = 'CAPACITA_FISCALE' then valore_num end) as capacita_fiscale,
    max(case when componente = 'FONDO_PEREQUATIVO' then valore_num end) as fondo_perequativo,
    max(case when componente = 'DOTAZIONE_FINALE_FSC' then valore_num end) as dotazione_finale_fsc,
    max(case when componente = 'IMU_TASI_STANDARD' then valore_num end) as imu_tasi_standard,
    max(case when componente = 'TOTALE_RISORSE_STORICHE' then valore_num end) as totale_risorse_storiche
  from parsed
  where componente in (
    'POPOLAZIONE', 'CAPACITA_FISCALE', 'FONDO_PEREQUATIVO',
    'DOTAZIONE_FINALE_FSC', 'IMU_TASI_STANDARD', 'TOTALE_RISORSE_STORICHE'
  )
  group by username
),
enti as (
  select *
  from read_parquet('{support.opencivitas_fsc_enti_rso.mart}')
)
select
  {year} as anno,
  fsc.username,
  enti.denominazione as comune,
  enti.provincia,
  enti.regione,
  enti.regione_istat_cod,
  fsc.popolazione,
  fsc.capacita_fiscale,
  fsc.fondo_perequativo,
  fsc.dotazione_finale_fsc,
  fsc.imu_tasi_standard,
  fsc.totale_risorse_storiche,
  enti.username is not null as join_enti_ok
from fsc
inner join enti on fsc.username = enti.username
where fsc.username is not null
order by enti.regione, enti.provincia, enti.denominazione
