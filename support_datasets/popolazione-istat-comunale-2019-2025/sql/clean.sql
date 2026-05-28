select
  {year}::INTEGER                                            as anno,
  trim(cast("Codice comune" as varchar)) as codice_comune,
  trim(cast("Comune" as varchar)) as comune,
  try_cast("Età" as integer) as eta,
  case
    when try_cast("Età" as integer) between 0 and 14 then '0-14'
    when try_cast("Età" as integer) between 15 and 29 then '15-29'
    when try_cast("Età" as integer) between 30 and 44 then '30-44'
    when try_cast("Età" as integer) between 45 and 59 then '45-59'
    when try_cast("Età" as integer) between 60 and 74 then '60-74'
    when try_cast("Età" as integer) >= 75 then '75+'
  end as fascia_eta,
  try_cast("Celibi" as integer) as celibi,
  try_cast("Coniugati" as integer) as coniugati,
  try_cast("Divorziati" as integer) as divorziati,
  try_cast("Vedovi" as integer) as vedovi,
  try_cast("Uniti civilmente" as integer) as uniti_civilmente_maschi,
  try_cast("Maschi già in unione civile (per scioglimento unione)" as integer) as maschi_gia_unione_civile_scioglimento,
  try_cast("Maschi già in unione civile (per decesso del partner)" as integer) as maschi_gia_unione_civile_decesso,
  try_cast("Totale maschi" as integer) as totale_maschi,
  try_cast("Nubili" as integer) as nubili,
  try_cast("Coniugate" as integer) as coniugate,
  try_cast("Divorziate" as integer) as divorziate,
  try_cast("Vedove" as integer) as vedove,
  try_cast("Unite civilmente" as integer) as unite_civilmente_femmine,
  try_cast("Femmine già in unione civile (per scioglimento unione)" as integer) as femmine_gia_unione_civile_scioglimento,
  try_cast("Femmine già in unione civile (per decesso del partner)" as integer) as femmine_gia_unione_civile_decesso,
  try_cast("Totale femmine" as integer) as totale_femmine,
  try_cast("Totale" as integer) as popolazione_residente
from raw_input
where try_cast("Età" as integer) <> 999
