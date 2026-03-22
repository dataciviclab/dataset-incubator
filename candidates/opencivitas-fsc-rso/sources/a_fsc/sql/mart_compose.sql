-- mart_compose.sql — compose minimo FSC 2025 eseguito da sources/a_fsc
--
-- Il layer compose e` documentato anche in candidates/opencivitas-fsc-rso/compose/.
-- Per vincolo del toolkit, l'SQL eseguibile resta agganciato al dataset di A.
--
-- DIPENDENZA: il mart di sources/b_enti deve essere gia` stato materializzato
-- prima di eseguire questo compose. Il toolkit non lo esegue automaticamente.
-- I read_parquet seguono l'effective_root del dataset tramite {root_posix}.

with fsc as (
  select *
  from read_parquet(
    '{root_posix}/data/mart/opencivitas_fsc_2025_rso/{year}/mart_fsc_comune.parquet'
  )
),
enti as (
  select *
  from read_parquet(
    '{root_posix}/data/mart/opencivitas_fsc_enti_rso/{year}/mart_enti.parquet'
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
