select
  anno_riferimento,
  regione_pa,
  provincia_pa,
  sigla_provincia_pa,
  tipologia_amministrazione,
  regione_fornitore,
  sum(valore_economico_consumi) as valore_economico_consumi_totale,
  sum(numero_ordini_con_consumi) as numero_ordini_totale,
  count(distinct convenzione) as numero_convenzioni_distinte,
  count(distinct lotto) as numero_lotti_distinti,
  sum(n_pa_con_consumi) as numero_pa_totale,
  sum(n_po_con_consumi) as numero_po_totale
from clean_input
group by
  anno_riferimento,
  regione_pa,
  provincia_pa,
  sigla_provincia_pa,
  tipologia_amministrazione,
  regione_fornitore
order by
  anno_riferimento,
  regione_pa,
  provincia_pa,
  tipologia_amministrazione
