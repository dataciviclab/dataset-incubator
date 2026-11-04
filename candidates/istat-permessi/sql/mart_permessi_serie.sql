-- mart_permessi_serie: permessi di soggiorno validi in Italia per anno
-- (serie storica nazionale, riga WORLD).
select
    anno,
    permessi as permessi_italia
from clean_input
where livello = 'nazionale' and cittadinanza_codice = 'WORLD' and permessi is not null
order by anno
