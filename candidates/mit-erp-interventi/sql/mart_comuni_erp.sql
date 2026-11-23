-- mart_comuni_erp: un comune per riga con la catena finanziato -> alloggi -> assegnati
-- ATTENZIONE: `alloggi_assegnati` puo' essere 0 sia per "non ancora assegnati" sia per
-- "non comunicato": il dataset non distingue. La quota e' un limite inferiore, non una
-- misura di efficacia.
select
    codice_istat_comune,
    any_value(comune) as comune,
    any_value(provincia) as provincia,
    any_value(regione) as regione,
    count(*) as interventi,
    round(sum(importo_intervento) / 1e6, 3) as importo_mln,
    sum(numero_alloggi) as alloggi_previsti,
    sum(alloggi_assegnati) as alloggi_assegnati,
    round(100.0 * sum(alloggi_assegnati) / nullif(sum(numero_alloggi), 0), 1) as quota_assegnati_pct,
    count(*) filter (where stato = 'Completato') as interventi_completati,
    count(*) filter (where stato = 'non più Realizzabile') as interventi_non_realizzabili,
    coalesce(sum(alloggi_assegnati) filter (where stato = 'Completato'), 0) as assegnati_da_completati
from clean_input
group by 1
having sum(numero_alloggi) > 0
order by alloggi_previsti desc
