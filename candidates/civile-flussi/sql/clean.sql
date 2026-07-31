select
  cast_int("Anno") as anno,
  normalize_string("Fonte") as fonte,
  normalize_string("Tipo ufficio") as tipo_ufficio,
  normalize_string("Distretto") as distretto,
  normalize_string("Sede") as sede,
  normalize_string("Macromateria") as macromateria,
  normalize_string("Materia") as materia,
  normalize_string("Dettaglio") as dettaglio,
  cast_double("Sopravvenuti") as sopravvenuti,
  cast_double("Definiti - totale") as definiti_totale,
  cast_double("Definiti con sentenza") as definiti_con_sentenza,
  cast_double("Pendenti finali") as pendenti_finali
from raw_input
where cast_int("Anno") is not null
  and coalesce(normalize_string("Fonte"), '') <> ''
