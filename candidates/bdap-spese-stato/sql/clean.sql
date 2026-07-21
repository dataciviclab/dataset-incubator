select
  cast_int(column00) as esercizio_finanziario,
  nullif(trim(column01), '') as stato_previsione,
  nullif(trim(column02), '') as amministrazione,
  nullif(trim(column03), '') as missione,
  nullif(trim(column04), '') as programma,
  nullif(trim(column05), '') as udv_livello_1,
  nullif(trim(column06), '') as udv_livello_2,
  nullif(trim(column07), '') as udv_livello_3,
  nullif(trim(column08), '') as codice_puntato_udv,
  nullif(trim(column09), '') as macroaggregato,
  cast_double(column10) as previsioni_definitive_cp,
  cast_double(column11) as previsioni_definitive_cs
from raw_input
where cast_int(column00) is not null
