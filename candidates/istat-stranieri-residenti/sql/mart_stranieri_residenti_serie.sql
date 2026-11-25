-- mart_stranieri_residenti_serie: stranieri residenti in Italia per anno
-- (serie storica nazionale, riga WORLD).
select
    anno,
    residenti as residenti_italia
from clean_input
where livello = 'nazionale' and cittadinanza_codice = 'WORLD' and residenti is not null
order by anno
