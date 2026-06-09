-- Mart: aggregazioni Gare Opere Pubbliche MOP per regione e tipologia

-- Mart 0: per regione
select
    cod_regione,
    desc_regione,
    count(*) as numero_gare,
    count(distinct codice_cup) as progetti_distinti,
    count(distinct codice_cig) as gare_distinte,
    count(distinct codice_fiscale_soggetto) as fornitori_distinti,
    count(distinct codice_ente) as enti_appaltanti_distinti,
    sum(numero_partecipanti_gara) as totale_partecipanti,
    avg(numero_partecipanti_gara) as media_partecipanti_per_gara,
    sum(importo_base_asta) as importo_totale_base_asta,
    sum(importo_aggiudicazione) as importo_totale_aggiudicazione,
    avg(importo_base_asta) as importo_medio_base_asta,
    avg(importo_aggiudicazione) as importo_medio_aggiudicazione
from clean_input
group by cod_regione, desc_regione
order by cod_regione
