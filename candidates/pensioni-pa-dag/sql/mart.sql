select
  anno,
  mese,
  regione,
  tipo_pensione,
  sum(numero_partite) as numero_partite,
  sum(importi_mensili_pagati_eur) as importi_mensili_pagati_eur,
  count(*) as righe_granulari
from clean_input
where mese = 12
  and tipo_pensione in ('DIRETTA', 'INDIRETTA/REVERSIBILE')
  and regione not in ('Italia', 'Estero')
group by 1, 2, 3, 4
order by anno desc, numero_partite desc, regione, tipo_pensione
