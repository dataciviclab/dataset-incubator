select
  trim("COD_LOCALE_PROGETTO") as cod_locale_progetto,
  trim("CUP") as cup,
  trim("OC_DESCR_CICLO") as ciclo,
  trim("OC_TEMA_SINTETICO") as tema_sintetico,
  trim("FONDO_COMUNITARIO") as fondo_comunitario,
  trim("DEN_REGIONE") as regione,
  trim("DEN_PROVINCIA") as provincia,
  trim("DEN_COMUNE") as comune,
  trim("OC_STATO_PROGETTO") as stato_progetto,
  try_cast(replace("FINANZ_UE", ',', '.') as double) as finanz_ue,
  try_cast(replace("FINANZ_TOTALE_PUBBLICO", ',', '.') as double) as finanz_totale_pubblico,
  try_cast(replace("TOT_PAGAMENTI", ',', '.') as double) as tot_pagamenti,
  try_cast(replace("OC_COSTO_COESIONE", ',', '.') as double) as costo_coesione,
  trim(cast("OC_DATA_INIZIO_PROGETTO" as varchar)) as data_inizio_progetto,
  trim(cast("OC_DATA_FINE_PROGETTO_PREVISTA" as varchar)) as data_fine_progetto_prevista,
  trim(cast("OC_DATA_FINE_PROGETTO_EFFETTIVA" as varchar)) as data_fine_progetto_effettiva
from raw_input
where trim(coalesce("OC_DESCR_CICLO", '')) = 'Ciclo di programmazione 2014-2020'
  and try_cast(replace("FINANZ_UE", ',', '.') as double) > 0
  and trim(coalesce("DEN_REGIONE", '')) <> ''
  and trim(coalesce("DEN_REGIONE", '')) <> 'AMBITO NAZIONALE'
  and trim(coalesce("DEN_REGIONE", '')) <> 'PAESI EUROPEI'
  and trim(coalesce("DEN_REGIONE", '')) not like '%:::%'
  and trim(coalesce("OC_TEMA_SINTETICO", '')) <> ''
