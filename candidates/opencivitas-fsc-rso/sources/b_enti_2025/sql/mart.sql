select distinct
  username,
  denominazione,
  provincia,
  regione,
  regione_istat_cod
from clean_input
where username is not null
