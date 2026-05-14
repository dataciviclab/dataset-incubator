select
  {year}::INTEGER                                            as anno,
  trim(replace(cast("IstatComune" as varchar), chr(9), '')) as codice_comune_istat,
  trim(cast("Regione" as varchar)) as regione,
  trim(cast("Provincia" as varchar)) as provincia,
  trim(cast("Comune" as varchar)) as comune,
  try_cast(replace(cast("Popolazione" as varchar), '.', '') as bigint) as popolazione,
  trim(cast("Dato riferito a" as varchar)) as dato_riferito_a,
  try_cast(replace(replace(cast("Totale RU (t)" as varchar), '.', ''), ',', '.') as double) as totale_ru_tonnellate,
  try_cast(replace(replace(cast("Totale RD (t)" as varchar), '.', ''), ',', '.') as double) as totale_rd_tonnellate,
  try_cast(replace(replace(replace(cast("Percentuale RD (%)" as varchar), '%', ''), '.', ''), ',', '.') as double) as percentuale_rd
from raw_input
where trim(replace(coalesce(cast("IstatComune" as varchar), ''), chr(9), '')) <> ''
  and trim(coalesce(cast("Dato riferito a" as varchar), '')) = 'Comune'
  and try_cast(replace(cast("Popolazione" as varchar), '.', '') as bigint) is not null
