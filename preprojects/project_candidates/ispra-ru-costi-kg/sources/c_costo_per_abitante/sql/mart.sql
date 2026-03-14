select
  codice_comune_istat,
  comune_o_aggregazione as comune,
  provincia,
  popolazione,
  crt_euro_ab,
  cts_euro_ab,
  crd_euro_ab,
  ctr_euro_ab,
  csl_euro_ab,
  cc_euro_ab,
  ck_euro_ab,
  altri_costi_euro_ab,
  ctot_euro_ab
from clean_input
where popolazione > 0
order by provincia, comune
