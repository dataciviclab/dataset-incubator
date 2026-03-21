select
  trim("USERNAME") as username,
  trim("Componenti di calcolo del fondo") as componente,
  trim(cast("Valore" as varchar)) as valore_raw,
  try_cast(replace(trim(cast("Valore" as varchar)), ',', '.') as double) as valore_num
from raw_input
where trim(coalesce("USERNAME", '')) <> ''
  and trim(coalesce("Componenti di calcolo del fondo", '')) <> ''
