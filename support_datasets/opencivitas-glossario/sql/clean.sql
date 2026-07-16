select
  trim(cast("codice_indicatore" as varchar)) as codice_indicatore,
  trim(cast("descrizione" as varchar)) as descrizione,
  trim(cast("tipo" as varchar)) as tipo,
  trim(cast("categoria" as varchar)) as categoria,
  trim(cast("funzione" as varchar)) as funzione,
  try_cast(trim(cast("ordine" as varchar)) as integer) as ordine,
  try_cast(trim(cast("anno" as varchar)) as integer) as anno,
  trim(cast("ambito" as varchar)) as ambito
from raw_input
where trim(coalesce(cast("codice_indicatore" as varchar), '')) <> ''
