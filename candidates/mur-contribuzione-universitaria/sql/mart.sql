select
    anno,
    cod_ateneo,
    nome_ateneo,
    codice_gettito,
    descrizione_gettito,
    sum(euro_contributo) as totale_euro,
    count(*) as n_righe
from clean_input
group by
    anno,
    cod_ateneo,
    nome_ateneo,
    codice_gettito,
    descrizione_gettito
order by
    anno,
    cod_ateneo,
    codice_gettito
