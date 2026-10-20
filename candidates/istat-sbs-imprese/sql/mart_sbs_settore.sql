-- mart_sbs_settore.sql
-- Matrice settoriale nazionale: un rigo per anno × sezione NACE.
-- Unità: migliaia di euro (mila_eur), migliaia di ore (migliaia),
-- euro per ora e percentuali.
-- Solo grain nazionale; esclude il totale 0010.

with x as (
    select
        anno,
        nace_codice,
        nace,
        max(case when indicatore_codice = '12150' then valore end) as va_mila_eur,
        max(case when indicatore_codice = '13310' then valore end) as costo_lavoro_mila_eur,
        max(case when indicatore_codice = '13320' then valore end) as salari_mila_eur,
        max(case when indicatore_codice = '13330' then valore end) as contributi_mila_eur,
        max(case when indicatore_codice = '12170' then valore end) as gos_mila_eur,
        max(case when indicatore_codice = '15110' then valore end) as investimenti_mila_eur,
        max(case when indicatore_codice = '16150' then valore end) as ore_migliaia
    from clean_input
    where grain = 'nazionale'
      and nace_codice <> '0010'
    group by anno, nace_codice, nace
)
select
    anno,
    nace_codice,
    nace,
    va_mila_eur,
    costo_lavoro_mila_eur,
    salari_mila_eur,
    contributi_mila_eur,
    gos_mila_eur,
    investimenti_mila_eur,
    ore_migliaia,
    case when ore_migliaia > 0 then va_mila_eur / ore_migliaia end as va_per_ora_eur,
    case when ore_migliaia > 0 then costo_lavoro_mila_eur / ore_migliaia end as costo_lavoro_per_ora_eur,
    case when ore_migliaia > 0 then salari_mila_eur / ore_migliaia end as salario_per_ora_eur,
    case when va_mila_eur > 0 then costo_lavoro_mila_eur / va_mila_eur * 100 end as quota_lavoro_pct,
    case when va_mila_eur > 0 then gos_mila_eur / va_mila_eur * 100 end as gos_su_va_pct,
    case when va_mila_eur > 0 then investimenti_mila_eur / va_mila_eur * 100 end as investimenti_su_va_pct,
    case when costo_lavoro_mila_eur > 0 then salari_mila_eur / costo_lavoro_mila_eur * 100 end as salari_su_costo_lavoro_pct,
    case when costo_lavoro_mila_eur > 0 then contributi_mila_eur / costo_lavoro_mila_eur * 100 end as contributi_su_costo_lavoro_pct
from x
order by anno, nace_codice
