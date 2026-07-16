-- mart.sql — arricchimento con comuni_master per chiavi standard
-- Aggiunge codice_istat, codice_catastale dal golden record
-- NOTA: provincia nel clean è codice ISTAT 3 cifre (es. '015')
--   il join usa substr(codice_istat, 1, 3) per matchare

with comuni as (
  select codice_istat, denominazione, codice_catastale, sigla_provincia,
         substr(codice_istat, 1, 3) as prov_cod
  from read_parquet('{support.comuni_master.mart}')
)
select
  c.*,
  cm.codice_istat,
  cm.codice_catastale
from clean_input c
left join comuni cm
  on upper(cm.denominazione) = upper(c.denominazione)
  and cm.prov_cod = c.provincia
