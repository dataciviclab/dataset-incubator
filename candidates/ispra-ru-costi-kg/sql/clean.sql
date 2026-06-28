select
  {year}::INTEGER                                            as anno,
  trim(replace(cast("IstatComune" as varchar), chr(9), '')) as codice_comune_istat,
  trim(cast("Comune o Aggregazione" as varchar)) as comune_o_aggregazione,
  trim(cast("Provincia" as varchar)) as provincia,
  try_cast(replace(cast("Numero di comuni" as varchar), '.', '') as bigint) as numero_comuni,
  try_cast(replace(cast("Pop.(abitanti)" as varchar), '.', '') as bigint) as popolazione,
  try_cast(replace(replace(cast("CRTkg" as varchar), '.', ''), ',', '.') as double) as crt_cent_kg,
  try_cast(replace(replace(cast("CRDkg" as varchar), '.', ''), ',', '.') as double) as crd_cent_kg,
  try_cast(replace(replace(cast("CSLkg" as varchar), '.', ''), ',', '.') as double) as csl_cent_kg,
  try_cast(replace(replace(cast("CCkg" as varchar), '.', ''), ',', '.') as double) as cc_cent_kg,
  try_cast(replace(replace(cast("CKkg" as varchar), '.', ''), ',', '.') as double) as ck_cent_kg,
  try_cast(replace(replace(cast("CTOTkg" as varchar), '.', ''), ',', '.') as double) as ctot_cent_kg
from raw_input
where trim(replace(coalesce(cast("IstatComune" as varchar), ''), chr(9), '')) <> ''
  and try_cast(replace(cast("Numero di comuni" as varchar), '.', '') as bigint) = 1
