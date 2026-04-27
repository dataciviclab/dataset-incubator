with base as (
  select
    anno,
    comparto,
    coalesce(donne_tempo_pieno, 0)
      + coalesce(donne_part_time_inf_50, 0)
      + coalesce(donne_part_time_sup_50, 0) as donne_totali,
    coalesce(uomini_tempo_pieno, 0)
      + coalesce(uomini_part_time_inf_50, 0)
      + coalesce(uomini_part_time_sup_50, 0) as uomini_totali,
    coalesce(donne_assunte, 0) + coalesce(uomini_assunti, 0) as assunti_totali,
    coalesce(donne_cessate, 0) + coalesce(uomini_cessati, 0) as cessati_totali
  from clean_input
)
select
  anno,
  comparto,
  sum(donne_totali + uomini_totali) as dipendenti_totali,
  sum(assunti_totali) as assunti_totali,
  sum(cessati_totali) as cessati_totali,
  sum(assunti_totali) - sum(cessati_totali) as saldo_netto,
  round(100.0 * sum(assunti_totali) / nullif(sum(donne_totali + uomini_totali), 0), 2) as tasso_assunzione_pct,
  round(100.0 * sum(cessati_totali) / nullif(sum(donne_totali + uomini_totali), 0), 2) as tasso_uscita_pct,
  round(100.0 * (sum(assunti_totali) + sum(cessati_totali)) / nullif(sum(donne_totali + uomini_totali), 0), 2) as tasso_turnover_lordo_pct,
  round(100.0 * sum(donne_totali) / nullif(sum(donne_totali + uomini_totali), 0), 2) as quota_donne_pct
from base
group by 1, 2
order by anno, dipendenti_totali desc

