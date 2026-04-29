select
  amministrazione_regione_sede as amministrazione_regione,
  amministrazione_provincia_sede as amministrazione_provincia,
  amministrazione_comune_sede as amministrazione_comune,
  amministrazione_categoria,
  count(*) as numero_partecipazioni,
  count(distinct amministrazione_codice_fiscale) as numero_amministrazioni,
  count(distinct partecipata_codice_fiscale) as numero_partecipate,
  round(100.0 * count(*) filter (where appartenenza_perimetro_tusp = 'SI') / count(*), 1) as pct_perimetro_tusp,
  round(100.0 * count(*) filter (where appartenenza_perimetro_revisione_periodica = 'SI') / count(*), 1) as pct_perimetro_revisione
from clean_input
group by amministrazione_regione_sede, amministrazione_provincia_sede, amministrazione_comune_sede, amministrazione_categoria
order by amministrazione_regione_sede, amministrazione_provincia_sede, amministrazione_comune_sede, amministrazione_categoria