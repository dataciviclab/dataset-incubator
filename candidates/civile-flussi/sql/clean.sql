select
  cast_int("Anno") as anno,
  normalize_string("Fonte") as fonte,
  trim("Tipo ufficio") as tipo_ufficio,
  normalize_string("Distretto") as distretto,
  normalize_string("Sede") as sede,
  normalize_string("Macromateria") as macromateria,
  normalize_string("Materia") as materia,
  normalize_string("Dettaglio") as dettaglio,
  cast_double("Sopravvenuti") as sopravvenuti,
  try_cast("Definiti - totale" as double) as definiti_totale,
  try_cast("Definiti con sentenza" as double) as definiti_con_sentenza,
  try_cast("Pendenti finali" as double) as pendenti_finali
from raw_input
where cast_int("Anno") is not null
  and trim(coalesce("Fonte", '')) <> ''