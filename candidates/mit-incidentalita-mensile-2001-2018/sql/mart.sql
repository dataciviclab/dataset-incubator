-- mart.sql - mit-incidentalita-mensile-2001-2018
--
-- Output minimo: serie mensile 2001-2018 con conteggi core e indici principali.
-- Gli indicatori derivati (percentuali e indici) vengono propagati dal clean
-- senza ricalcolo: sono prodotti dalla fonte MIT sui dati originali completi
-- e non sono ricalcolabili con precisione dal solo perimetro mensile filtrato.
-- Usarli come riferimento orientativo, non per confronti puntuali.

select
    anno,
    mese,
    case mese
        when 'Gennaio'   then 1  when 'Febbraio'  then 2
        when 'Marzo'     then 3  when 'Aprile'    then 4
        when 'Maggio'    then 5  when 'Giugno'    then 6
        when 'Luglio'    then 7  when 'Agosto'    then 8
        when 'Settembre' then 9  when 'Ottobre'   then 10
        when 'Novembre'  then 11 when 'Dicembre'  then 12
    end                          as mese_num,
    incidenti,
    morti,
    feriti,
    incidenti_mortali,
    indice_mortalita,
    indice_gravita,
    indice_lesivita
from clean_input
order by anno, mese_num
