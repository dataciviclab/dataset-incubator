select
  {year}::INTEGER as anno_riferimento,
  trim("Tipologia_Amministrazione") as tipologia_amministrazione,
  trim("Regione_PA") as regione_pa,
  trim("Provincia_PA") as provincia_pa,
  trim("Sigla_provincia_PA") as sigla_provincia_pa,
  trim("Regione_Fornitore") as regione_fornitore,
  trim("Convenzione") as convenzione,
  trim("Lotto") as lotto,
  try_cast(replace(trim("Valore_economico_consumi"), ',', '.') as double) as valore_economico_consumi,
  "Numero_Ordini_con_consumi"::BIGINT as numero_ordini_con_consumi,
  "N_PA_con_consumi"::BIGINT as n_pa_con_consumi,
  "N_PO_con_consumi"::BIGINT as n_po_con_consumi
from raw_input
