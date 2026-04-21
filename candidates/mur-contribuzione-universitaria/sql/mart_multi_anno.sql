select
    anno,
    cod_ateneo,
    nome_ateneo,
    codice_gettito,
    descrizione_gettito,
    totale_euro,
    n_righe
from mart
order by
    anno,
    cod_ateneo,
    codice_gettito
