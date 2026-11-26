-- mart_territori_dicembre.sql: stock DAG a dicembre per territorio e tipo.
--
-- Include TUTTI i territori della fonte: le 20 regioni, l'ufficio centrale
-- "Italia" (ROMA - MEF DST UFFICIO V) e "Estero". Non sono aggregati: sono
-- componenti reali dello stock. Con l'inclusione, la somma del mart coincide
-- con il totale del clean.
--
-- Include tutti i tipi di pensione: DIRETTA, INDIRETTA/REVERSIBILE e la
-- trascurabile UNA TANTUM (1-2 partite nel 2017-2018/2022).
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
group by 1, 2, 3, 4
order by anno desc, numero_partite desc, regione, tipo_pensione
