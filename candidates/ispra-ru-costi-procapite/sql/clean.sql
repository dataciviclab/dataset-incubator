select
  {year}::INTEGER                                            as anno,
  trim(replace(cast("IstatComune" as varchar), chr(9), '')) as codice_comune_istat,
  trim(cast("Comune o Aggregazione" as varchar)) as comune_o_aggregazione,
  trim(cast("Provincia" as varchar)) as provincia,
  try_cast(replace(cast("Numero di comuni" as varchar), '.', '') as bigint) as numero_comuni,
  try_cast(replace(cast("Pop.(abitanti)" as varchar), '.', '') as bigint) as popolazione,
  try_cast(replace(replace(cast("CRTab" as varchar), '.', ''), ',', '.') as double) as crt_euro_ab,
  try_cast(replace(replace(cast("CTSab" as varchar), '.', ''), ',', '.') as double) as cts_euro_ab,
  try_cast(replace(replace(cast("CRDab" as varchar), '.', ''), ',', '.') as double) as crd_euro_ab,
  try_cast(replace(replace(cast("CTRab" as varchar), '.', ''), ',', '.') as double) as ctr_euro_ab,
  try_cast(replace(replace(cast("CSLab" as varchar), '.', ''), ',', '.') as double) as csl_euro_ab,
  try_cast(replace(replace(cast("CCab" as varchar), '.', ''), ',', '.') as double) as cc_euro_ab,
  try_cast(replace(replace(cast("CKab" as varchar), '.', ''), ',', '.') as double) as ck_euro_ab,
  try_cast(replace(replace(cast("Altri costi" as varchar), '.', ''), ',', '.') as double) as altri_costi_euro_ab,
  try_cast(replace(replace(cast("CTOTab" as varchar), '.', ''), ',', '.') as double) as ctot_euro_ab
from raw_input
where trim(replace(coalesce(cast("IstatComune" as varchar), ''), chr(9), '')) <> ''
  and try_cast(replace(cast("Numero di comuni" as varchar), '.', '') as bigint) = 1
