select
  cast_int(column00) as esercizio_finanziario,
  nullif(trim(column01), '') as codice_titolo,
  nullif(trim(column02), '') as titolo,
  nullif(trim(column03), '') as codice_natura,
  nullif(trim(column04), '') as natura,
  nullif(trim(column05), '') as codice_tipologia,
  nullif(trim(column06), '') as tipologia,
  nullif(trim(column07), '') as codice_provento,
  nullif(trim(column08), '') as provento,
  cast_double(column09) as previsioni_definitive_cp,
  cast_double(column10) as previsioni_definitive_cs
from raw_input
where cast_int(column00) is not null
