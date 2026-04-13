select
  try_cast(column00 as integer) as esercizio_finanziario,
  nullif(trim(column01), '') as codice_titolo,
  nullif(trim(column02), '') as titolo,
  nullif(trim(column03), '') as codice_natura,
  nullif(trim(column04), '') as natura,
  nullif(trim(column05), '') as codice_tipologia,
  nullif(trim(column06), '') as tipologia,
  nullif(trim(column07), '') as codice_provento,
  nullif(trim(column08), '') as provento,
  try_cast(column09 as double) as previsioni_definitive_cp,
  try_cast(column10 as double) as previsioni_definitive_cs
from raw_input
where try_cast(column00 as integer) between 2008 and 2024
  and nullif(trim(column01), '') is not null
  and nullif(trim(column03), '') is not null
  and nullif(trim(column05), '') is not null
