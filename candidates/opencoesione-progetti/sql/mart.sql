select
  OC_DESCR_CICLO as ciclo,
  OC_MACROAREA as macroarea,
  OC_TEMA_SINTETICO as tema,
  count(*) as n_progetti,
  sum(FINANZ_UE) as finanz_ue_tot,
  sum(FINANZ_STATO_FSC) as finanz_fsc_tot,
  sum(FINANZ_TOTALE_PUBBLICO) as finanz_tot_pub,
  sum(OC_COSTO_COESIONE) as costo_coesione,
  sum(IMPEGNI) as impegni_tot,
  sum(TOT_PAGAMENTI) as pagamenti_tot,
  case
    when sum(OC_COSTO_COESIONE) > 0
    then sum(TOT_PAGAMENTI) / sum(OC_COSTO_COESIONE)
    else null
  end as ratio_spesa,
  case
    when sum(OC_COSTO_COESIONE) > 0
    then sum(IMPEGNI) / sum(OC_COSTO_COESIONE)
    else null
  end as ratio_impegni
from clean_input
group by 1, 2, 3
order by ciclo, macroarea, tema
