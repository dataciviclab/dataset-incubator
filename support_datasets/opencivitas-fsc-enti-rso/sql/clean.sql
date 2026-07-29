select
  trim(cast("USERNAME" as varchar)) as username,
  trim(cast("DENOMINAZIONE" as varchar)) as denominazione,
  trim(cast("PROVINCIA" as varchar)) as provincia,
  trim(cast("REGIONE_DES" as varchar)) as regione,
  try_cast("REGIONE_ISTAT_COD" as integer) as regione_istat_cod
from raw_input
where trim(coalesce(cast("USERNAME" as varchar), '')) <> ''
