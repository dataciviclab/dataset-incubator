select
    anno,
    trimestre,
    area_geografica,
    regione,
    sesso,
    classe_eta,
    classe_importo,
    sum(numero_pensioni) as numero_pensioni
from clean_input
group by 1, 2, 3, 4, 5, 6, 7
order by anno, trimestre, regione, sesso, classe_eta, classe_importo;
