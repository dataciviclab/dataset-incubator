-- mart_trend — ospiti totali e anziani non autosufficienti: trend multi-anno
-- per area (Italia + 20 regioni/PA). Il clean contiene 2009-2023, quindi il
-- trend si calcola senza glob multi-anno.

with yearly as (
    select
        anno,
        ref_area_codice,
        regione,
        max(case
            when tipo_dato_codice = '80' and eta_codice = 'TOTAL'
             and bisogno_codice = 'ALL' and livello_assistenza_codice = 'ALL'
            then ospiti
        end) as ospiti_totali,
        max(case
            when tipo_dato_codice = '89' and eta_codice = 'Y_GE65'
             and bisogno_codice = 'NOSELSUFELD' and livello_assistenza_codice = 'ALL'
            then ospiti
        end) as ospiti_non_auto
    from clean_input
    where ref_area_codice = 'IT'
       or (length(ref_area_codice) = 4 and ref_area_codice <> 'ITDA')
    group by anno, ref_area_codice, regione
),
valid as (
    select * from yearly where ospiti_totali is not null
),
ranked as (
    select
        *,
        row_number() over (partition by ref_area_codice order by anno) as rn_first,
        row_number() over (partition by ref_area_codice order by anno desc) as rn_last
    from valid
),
first_last as (
    select
        f.ref_area_codice,
        f.regione,
        f.anno as first_year,
        l.anno as last_year,
        f.ospiti_totali as ospiti_totali_first,
        l.ospiti_totali as ospiti_totali_last,
        f.ospiti_non_auto as ospiti_non_auto_first,
        l.ospiti_non_auto as ospiti_non_auto_last
    from ranked f
    join ranked l on f.ref_area_codice = l.ref_area_codice
    where f.rn_first = 1 and l.rn_last = 1
)

select
    ref_area_codice,
    regione,
    first_year,
    last_year,
    (last_year - first_year) as years_observed,
    ospiti_totali_first,
    ospiti_totali_last,
    (ospiti_totali_last - ospiti_totali_first) as delta_abs,
    round((ospiti_totali_last / nullif(ospiti_totali_first, 0) - 1) * 100, 1) as delta_pct,
    case
        when last_year > first_year and ospiti_totali_first > 0
        then round((power(
                ospiti_totali_last / ospiti_totali_first,
                1.0 / (last_year - first_year)
            ) - 1) * 100, 2)
    end as cagr_pct,
    ospiti_non_auto_first,
    ospiti_non_auto_last,
    case
        when last_year > first_year and ospiti_non_auto_first > 0
        then round((power(
                ospiti_non_auto_last / ospiti_non_auto_first,
                1.0 / (last_year - first_year)
            ) - 1) * 100, 2)
    end as cagr_non_auto_pct
from first_last
order by ref_area_codice
