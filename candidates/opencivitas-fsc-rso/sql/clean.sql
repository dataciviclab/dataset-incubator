-- clean.sql — FSC 2025: pivot EAV→wide + join geografico
--
-- Trasforma il formato long (username, componente, valore_num) in formato wide
-- con le 6 componenti FSC principali. Arricchisce con geografia dal support dataset.
--
-- Il support dataset (opencivitas-fsc-enti-rso) viene eseguito automaticamente
-- prima del main grazie alla sezione support: in dataset.yml.

with parsed as (
  select
    trim("USERNAME") as username,
    trim("Componenti di calcolo del fondo") as componente,
    try_cast(replace(trim(cast("Valore" as varchar)), ',', '.') as double) as valore_num
  from raw_input
  where trim(coalesce("USERNAME", '')) <> ''
    and trim(coalesce("Componenti di calcolo del fondo", '')) <> ''
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
left join enti on fsc.username = enti.username
where fsc.username is not null
order by enti.regione, enti.provincia, enti.denominazione
