-- mart_cittadinanze_serie: acquisizioni di cittadinanza in Italia per anno x
-- processo di acquisizione (serie storica nazionale, riga WORLD).
select
    anno,
    processo_codice,
    processo,
    acquisizioni as acquisizioni_italia
from clean_input
where livello = 'nazionale' and cittadinanza_codice = 'WORLD' and acquisizioni is not null
order by anno, processo_codice
