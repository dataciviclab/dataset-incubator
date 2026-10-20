-- mart_sbs_filiere.sql
-- Matrice nazionale delle filiere agroalimentari: NACE 10 (alimentare),
-- 11 (bevande), 12 (tabacco), 47 (commercio al dettaglio).
-- Unità: migliaia di euro, migliaia di ore, euro/ora, percentuali.
-- L'agricoltura (NACE A/01) non è coperta da SBS: per quella usare RICA.

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
        max(case when indicatore_codice = '16150' then valore end) as ore_migliaia,
        max(case when indicatore_codice = '11110' then valore end) as imprese
    from clean_input
    where grain = 'nazionale'
      and size_class = 'Totale'
      and nace_codice in ('10', '11', '12', '47')
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
    imprese,
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
