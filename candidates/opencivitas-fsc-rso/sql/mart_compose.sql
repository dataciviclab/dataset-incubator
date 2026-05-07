-- mart_compose.sql — FSC 2025 con geografia da support
--
-- Legge clean_input (FSC long) + support mart (enti geografici).
-- Il support gira automaticamente prima del main via support: in dataset.yml.

with fsc as (
  select
    username,
    max(case when componente = 'POPOLAZIONE' then valore_num end) as popolazione,
    max(case when componente = 'CAPACITA_FISCALE' then valore_num end) as capacita_fiscale,
    max(case when componente = 'FONDO_PEREQUATIVO' then valore_num end) as fondo_perequativo,
    max(case when componente = 'DOTAZIONE_FINALE_FSC' then valore_num end) as dotazione_finale_fsc,
    max(case when componente = 'IMU_TASI_STANDARD' then valore_num end) as imu_tasi_standard,
    max(case when componente = 'TOTALE_RISORSE_STORICHE' then valore_num end) as totale_risorse_storiche
  from clean_input
  where componente in (
    'POPOLAZIONE',
    'CAPACITA_FISCALE',
    'FONDO_PEREQUATIVO',
    'DOTAZIONE_FINALE_FSC',
    'IMU_TASI_STANDARD',
    'TOTALE_RISORSE_STORICHE'
  )
  group by 1
),
enti as (
  select *
  from read_parquet(
    '{root}/data/mart/opencivitas_fsc_enti_rso/{year}/mart_enti.parquet'
  )
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
  case
    when fsc.popolazione is not null and fsc.popolazione <> 0
      then fsc.capacita_fiscale / fsc.popolazione
    else null
  end as capacita_fiscale_procapite,
  case
    when fsc.popolazione is not null and fsc.popolazione <> 0
      then fsc.fondo_perequativo / fsc.popolazione
    else null
  end as fondo_perequativo_procapite,
  case
    when fsc.popolazione is not null and fsc.popolazione <> 0
      then fsc.dotazione_finale_fsc / fsc.popolazione
    else null
  end as dotazione_finale_fsc_procapite,
  enti.username is not null as join_enti_ok
from fsc
left join enti
  on fsc.username = enti.username
where fsc.username is not null
order by enti.regione, enti.provincia, enti.denominazione
