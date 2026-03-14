select
  codice_comune_istat,
  comune_o_aggregazione as comune,
  provincia,
  popolazione,
  crt_cent_kg,
  crd_cent_kg,
  csl_cent_kg,
  cc_cent_kg,
  ck_cent_kg,
  ctot_cent_kg
from clean_input
where popolazione > 0
order by provincia, comune
