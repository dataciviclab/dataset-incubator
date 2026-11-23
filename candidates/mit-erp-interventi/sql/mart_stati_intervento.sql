-- mart_stati_intervento: quadro nazionale per stato del monitoraggio
select
    stato,
    count(*) as interventi,
    round(sum(importo_intervento) / 1e6, 3) as importo_mln,
    sum(numero_alloggi) as alloggi_previsti,
    sum(alloggi_assegnati) as alloggi_assegnati,
    round(100.0 * sum(alloggi_assegnati) / nullif(sum(numero_alloggi), 0), 1) as quota_assegnati_pct,
    count(*) filter (where data_fine_lavori is not null) as con_data_fine_lavori,
    round(median(durata_lavori_giorni), 0) as durata_mediana_giorni
from clean_input
group by 1
order by alloggi_previsti desc
