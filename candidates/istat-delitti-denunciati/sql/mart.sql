select
    anno,
    codice_territorio,
    territorio,
    codice_reato,
    reato,
    numero_denunce
from clean_input
order by anno, codice_territorio, codice_reato
