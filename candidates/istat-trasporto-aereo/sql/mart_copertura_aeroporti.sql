-- mart_copertura_aeroporti.sql: profilo di copertura per aeroporto (righe, anni, tipo dato).
select aeroporto, unita, count(*) as osservazioni, min(anno) as primo, max(anno) as ultimo
from clean_input
group by 1, 2
order by osservazioni desc
