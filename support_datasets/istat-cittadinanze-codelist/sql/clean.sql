-- clean.sql: codelist cittadinanza ISTAT (support condiviso)
select
    normalize_string(codice) as codice,
    normalize_string(nome) as nome,
    normalize_string(tipo) as tipo
from raw_input
where codice is not null
