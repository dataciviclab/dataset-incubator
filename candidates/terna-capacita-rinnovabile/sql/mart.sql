select
    anno,
    regione,
    fonti,
    sum(potenza_mw) as potenza_totale_mw,
    count(*) as record_count
from clean_input
where tipo_capacita = 'Netta'
group by 1, 2, 3
order by anno, potenza_totale_mw desc, regione, fonti
