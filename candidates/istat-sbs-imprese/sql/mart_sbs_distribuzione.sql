-- mart_sbs_distribuzione.sql
-- Distribuzione dentro i settori: quartili Q1/Q2/Q3 per anno × NACE.
-- Unità: migliaia di euro (VA per addetto, costo per dipendente);
-- N00001 è un indice di produttività aggiustata per i salari.
-- Solo nazionale e classe Totale; esclude il totale 0010.

with x as (
    select
        anno,
        nace_codice,
        nace,
        max(case when indicatore_codice = 'E12150_PER_ADD_Q1' then valore end) as va_per_addetto_q1,
        max(case when indicatore_codice = 'E12150_PER_ADD_Q2' then valore end) as va_per_addetto_q2,
        max(case when indicatore_codice = 'E12150_PER_ADD_Q3' then valore end) as va_per_addetto_q3,
        max(case when indicatore_codice = 'E13310_PER_DIP_Q1' then valore end) as costo_personale_dipendente_q1,
        max(case when indicatore_codice = 'E13310_PER_DIP_Q2' then valore end) as costo_personale_dipendente_q2,
        max(case when indicatore_codice = 'E13310_PER_DIP_Q3' then valore end) as costo_personale_dipendente_q3,
        max(case when indicatore_codice = 'N00001_Q1' then valore end) as wage_adjusted_labour_productivity_q1,
        max(case when indicatore_codice = 'N00001_Q2' then valore end) as wage_adjusted_labour_productivity_q2,
        max(case when indicatore_codice = 'N00001_Q3' then valore end) as wage_adjusted_labour_productivity_q3
    from clean_input
    where grain = 'nazionale'
      and size_class = 'Totale'
      and nace_codice <> '0010'
    group by anno, nace_codice, nace
)
select
    anno,
    nace_codice,
    nace,
    va_per_addetto_q1,
    va_per_addetto_q2,
    va_per_addetto_q3,
    costo_personale_dipendente_q1,
    costo_personale_dipendente_q2,
    costo_personale_dipendente_q3,
    wage_adjusted_labour_productivity_q1,
    wage_adjusted_labour_productivity_q2,
    wage_adjusted_labour_productivity_q3,
    case when va_per_addetto_q1 > 0 then va_per_addetto_q3 / va_per_addetto_q1 end as rapporto_q3_q1_va,
    case when costo_personale_dipendente_q1 > 0 then costo_personale_dipendente_q3 / costo_personale_dipendente_q1 end as rapporto_q3_q1_costo
from x
order by anno, nace_codice
