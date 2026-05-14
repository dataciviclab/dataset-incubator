select
  anno,
  codice_comune_istat,
  regione,
  provincia,
  comune,
  popolazione,
  totale_ru_tonnellate,
  totale_rd_tonnellate,
  percentuale_rd,
  round(totale_ru_tonnellate * 1000.0 / nullif(popolazione, 0), 3) as kg_ru_per_abitante_calc,
  round(totale_rd_tonnellate * 1000.0 / nullif(popolazione, 0), 3) as kg_rd_per_abitante_calc
from clean_input
where popolazione > 0
order by anno, regione, provincia, comune
