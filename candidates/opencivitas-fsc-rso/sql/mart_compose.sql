-- mart_compose.sql — metriche derivate FSC 2025
--
-- Il pivot e il join geografico sono già stati fatti nel CLEAN.
-- Qui aggiungiamo solo le metriche procapite derivate.
-- clean_input è già wide con geografia.

select
  username,
  comune, provincia, regione, regione_istat_cod,
  popolazione,
  capacita_fiscale,
  fondo_perequativo,
  dotazione_finale_fsc,
  imu_tasi_standard,
  totale_risorse_storiche,
  join_enti_ok,
  case
    when popolazione is not null and popolazione <> 0
      then capacita_fiscale / popolazione
    else null
  end as capacita_fiscale_procapite,
  case
    when popolazione is not null and popolazione <> 0
      then fondo_perequativo / popolazione
    else null
  end as fondo_perequativo_procapite,
  case
    when popolazione is not null and popolazione <> 0
      then dotazione_finale_fsc / popolazione
    else null
  end as dotazione_finale_fsc_procapite
from clean_input
order by regione, provincia, comune
