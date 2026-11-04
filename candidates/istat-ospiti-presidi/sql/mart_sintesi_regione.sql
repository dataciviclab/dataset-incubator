-- mart_sintesi_regione — una riga per area (Italia + 20 regioni/PA) e anno.
-- Ospiti totali, anziani 65+, anziani autosufficienti/non, stranieri.
-- Esclude ripartizioni e aggregato ITDA per non duplicare le regioni.

with sintesi as (
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
             and bisogno_codice = 'ALL' and livello_assistenza_codice = 'ALL'
            then ospiti
        end) as ospiti_65plus,
        max(case
            when tipo_dato_codice = '89' and eta_codice = 'Y_GE65'
             and bisogno_codice = 'NOSELSUFELD' and livello_assistenza_codice = 'ALL'
            then ospiti
        end) as ospiti_65plus_non_autosufficienti,
        max(case
            when tipo_dato_codice = '89' and eta_codice = 'Y_GE65'
             and bisogno_codice = 'SELSUFELD' and livello_assistenza_codice = 'ALL'
            then ospiti
        end) as ospiti_65plus_autosufficienti,
        max(case
            when tipo_dato_codice = '92' and eta_codice = 'TOTAL'
             and bisogno_codice = 'ALL' and livello_assistenza_codice = 'ALL'
            then ospiti
        end) as ospiti_stranieri
    from clean_input
    where ref_area_codice = 'IT'
       or (length(ref_area_codice) = 4 and ref_area_codice <> 'ITDA')
    group by anno, ref_area_codice, regione
)

select
    anno,
    ref_area_codice,
    regione,
    ospiti_totali,
    ospiti_65plus,
    ospiti_65plus_non_autosufficienti,
    ospiti_65plus_autosufficienti,
    case
        when ospiti_65plus is not null and ospiti_65plus > 0
        then round(100.0 * ospiti_65plus_non_autosufficienti / ospiti_65plus, 1)
    end as quota_non_autosufficienti_pct,
    ospiti_stranieri,
    case
        when ospiti_totali is not null and ospiti_totali > 0
        then round(100.0 * ospiti_stranieri / ospiti_totali, 1)
    end as quota_stranieri_pct,
    case
        when ospiti_totali is not null and ospiti_totali > 0
        then round(100.0 * ospiti_65plus / ospiti_totali, 1)
    end as quota_65plus_pct
from sintesi
order by anno, ref_area_codice
