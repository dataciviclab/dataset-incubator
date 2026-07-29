with raw as (
  select
    trim(cast("USERNAME" as varchar)) as username,
    trim(cast("DENOMINAZIONE" as varchar)) as denominazione_orig,
    trim(cast("PROVINCIA" as varchar)) as provincia,
    trim(cast("REGIONE_DES" as varchar)) as regione,
    try_cast("REGIONE_ISTAT_COD" as integer) as regione_istat_cod
  from raw_input
  where trim(coalesce(cast("USERNAME" as varchar), '')) <> ''
)
select
  username,
  -- Normalizza apostrofo finale → accento (es. CANTU' → CANTÙ)
  -- La fonte FSC usa apostrofo ' al posto degli accenti sulle vocali finali (76 comuni su 6573)
  -- Sostituisce il bigramma VOCALE+' con la corrispondente vocale accentata
  CASE
    WHEN denominazione_orig LIKE '%U''' THEN REPLACE(denominazione_orig, 'U''', chr(217))  -- U' → Ù
    WHEN denominazione_orig LIKE '%O''' THEN REPLACE(denominazione_orig, 'O''', chr(210))  -- O' → Ò
    WHEN denominazione_orig LIKE '%I''' THEN REPLACE(denominazione_orig, 'I''', chr(204))  -- I' → Ì
    WHEN denominazione_orig LIKE '%E''' THEN REPLACE(denominazione_orig, 'E''', chr(200))  -- E' → È
    WHEN denominazione_orig LIKE '%A''' THEN REPLACE(denominazione_orig, 'A''', chr(192))  -- A' → À
    ELSE denominazione_orig
  END AS denominazione,
  provincia,
  regione,
  regione_istat_cod
from raw
