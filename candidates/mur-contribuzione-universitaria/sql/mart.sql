select
    cod_ateneo,
    nome_ateneo,
    codice_gettito,
    descrizione_gettito,
    sum(euro_contributo) as totale_euro,
    count(*) as n_righe
from clean_input
group by
    cod_ateneo,
    nome_ateneo,
    codice_gettito,
    descrizione_gettito
order by
    cod_ateneo,
    codice_gettito