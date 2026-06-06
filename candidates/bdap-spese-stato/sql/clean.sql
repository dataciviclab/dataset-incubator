select
  try_cast(column00 as integer) as esercizio_finanziario,
  nullif(trim(column01), '') as stato_previsione,
  nullif(trim(column02), '') as amministrazione,
  nullif(trim(column03), '') as missione,
  nullif(trim(column04), '') as programma,
  nullif(trim(column05), '') as udv_livello_1,
  nullif(trim(column06), '') as udv_livello_2,
  nullif(trim(column07), '') as udv_livello_3,
  nullif(trim(column08), '') as codice_puntato_udv,
  nullif(trim(column09), '') as macroaggregato,
  try_cast(column10 as double) as previsioni_definitive_cp,
  try_cast(column11 as double) as previsioni_definitive_cs
from raw_input
where try_cast(column00 as integer) is not null
