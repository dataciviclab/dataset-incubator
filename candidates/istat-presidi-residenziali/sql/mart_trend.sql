-- mart_trend — posti letto residenziali per 100.000 residenti: trend multi-anno
-- per area (Italia + 20 regioni/province autonome).
--
-- Il clean contiene l'intera serie 2009-2023, quindi il trend si calcola senza
-- glob multi-anno. Per ogni area:
--   • primo/ultimo anno con dato e valori di posti letto per 100k
--   • delta assoluto e relativo sulla finestra osservata
--   • CAGR quando la finestra ha piu' di un anno
--   • quota posti letto anziani (ELD) al primo e all'ultimo anno

with yearly as (
    select
        anno,
        ref_area_codice,
        regione,
        max(case
            when tipo_dato_codice = '75' and tipo_utenza_codice = 'TOT'
            then valore
        end) as posti_letto_per_100k,
        max(case
            when tipo_dato_codice = '73'
             and tipo_utenza_codice = 'TOT'
             and tipo_residenzialita_codice = 'ALL'
             and funzione_protezione_sociale_codice = '99'
             and livello_assistenza_codice = 'ALL'
             and natura_giuridica_codice = '9'
             and tipo_gestore_codice = 'TOT'
             and finanziamento_pubblico_codice = '9'
             and professione_codice = 'ALL'
            then valore
        end) as posti_letto,
        max(case
            when tipo_dato_codice = '73'
             and tipo_utenza_codice = 'ELD'
             and tipo_residenzialita_codice = 'ALL'
             and funzione_protezione_sociale_codice = '99'
             and livello_assistenza_codice = 'ALL'
             and natura_giuridica_codice = '9'
             and tipo_gestore_codice = 'TOT'
             and finanziamento_pubblico_codice = '9'
             and professione_codice = 'ALL'
            then valore
        end) as posti_letto_anziani
    from clean_input
    where ref_area_codice = 'IT'
       or (length(ref_area_codice) = 4 and ref_area_codice <> 'ITDA')
    group by anno, ref_area_codice, regione
),
with_quota as (
    select
        *,
        case
            when posti_letto is not null and posti_letto > 0
            then round(100.0 * posti_letto_anziani / posti_letto, 1)
        end as quota_anziani_pct
    from yearly
),
valid as (
    select * from with_quota where posti_letto_per_100k is not null
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
        f.posti_letto_per_100k as posti_letto_per_100k_first,
        l.posti_letto_per_100k as posti_letto_per_100k_last,
        f.quota_anziani_pct as quota_anziani_pct_first,
        l.quota_anziani_pct as quota_anziani_pct_last
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
    posti_letto_per_100k_first,
    posti_letto_per_100k_last,
    round(posti_letto_per_100k_last - posti_letto_per_100k_first, 2) as delta_abs,
    round((posti_letto_per_100k_last / nullif(posti_letto_per_100k_first, 0) - 1) * 100, 1) as delta_pct,
    case
        when last_year > first_year and posti_letto_per_100k_first > 0
        then round((power(
                posti_letto_per_100k_last / posti_letto_per_100k_first,
                1.0 / (last_year - first_year)
            ) - 1) * 100, 2)
    end as cagr_pct,
    quota_anziani_pct_first,
    quota_anziani_pct_last
from first_last
order by ref_area_codice
