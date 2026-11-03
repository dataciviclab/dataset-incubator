-- clean.sql: codelist territoriale ISTAT (support condiviso)
select
    normalize_string(ref_area) as ref_area,
    normalize_string(nome) as nome,
    normalize_string(livello) as livello
from raw_input
where ref_area is not null
