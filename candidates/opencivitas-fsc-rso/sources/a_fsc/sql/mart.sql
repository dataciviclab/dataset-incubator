with pivoted as (
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
)
select
  username,
  popolazione,
  capacita_fiscale,
  fondo_perequativo,
  dotazione_finale_fsc,
  imu_tasi_standard,
  totale_risorse_storiche
from pivoted
where username is not null
