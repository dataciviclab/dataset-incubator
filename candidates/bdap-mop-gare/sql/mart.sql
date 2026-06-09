-- Mart: statistiche Gare Opere Pubbliche MOP

select
    count(*) as numero_gare,
    count(distinct codice_cig) as gare_distinte,
    count(distinct codice_cup) as progetti_distinti,
    count(distinct codice_fiscale_soggetto) as fornitori_distinti,
    count(distinct codice_ente) as enti_appaltanti,
    sum(numero_partecipanti_gara) as totale_partecipanti,
    avg(numero_partecipanti_gara) as media_partecipanti,
    sum(importo_base_asta) as importo_totale_base_asta,
    sum(importo_aggiudicazione) as importo_totale_aggiudicato,
    avg(importo_base_asta) as importo_medio_base_asta,
    avg(importo_aggiudicazione) as importo_medio_aggiudicato
from clean_input
