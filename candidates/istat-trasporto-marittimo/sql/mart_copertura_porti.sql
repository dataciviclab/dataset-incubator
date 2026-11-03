-- mart_copertura_porti.sql: profilo di copertura per regione marittima di sbarco.
select regione_sbarco, unita, count(*) as osservazioni, min(anno) as primo, max(anno) as ultimo
from clean_input
group by 1, 2
order by osservazioni desc
