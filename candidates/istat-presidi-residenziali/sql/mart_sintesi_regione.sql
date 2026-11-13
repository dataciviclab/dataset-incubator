-- mart_sintesi_regione — una riga per area (Italia + 20 regioni/province autonome)
-- per l'anno del run. Metriche di totale: presidi, posti letto, personale.
-- Esclude le ripartizioni (ITC/ITD/ITE/ITF/ITG) e l'aggregato ITDA per non
-- duplicare le regioni.

with tot as (
    select
        anno,
        ref_area_codice,
        regione,
        max(case
            when tipo_dato_codice = '70' and finanziamento_pubblico_codice = '9'
            then valore
        end) as n_presidi,
        max(case
            when tipo_dato_codice = '72'
            then valore
        end) as presidi_per_100k,
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
            when tipo_dato_codice = '75' and tipo_utenza_codice = 'TOT'
            then valore
        end) as posti_letto_per_100k,
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
        end) as posti_letto_anziani,
        max(case
            when tipo_dato_codice = '76' and professione_codice = 'ALL'
            then valore
        end) as personale_retribuito,
        max(case
            when tipo_dato_codice = '78'
            then valore
        end) as personale_volontario
    from clean_input
    where ref_area_codice = 'IT'
       or (length(ref_area_codice) = 4 and ref_area_codice <> 'ITDA')
    group by anno, ref_area_codice, regione
)

select
    anno,
    ref_area_codice,
    regione,
    n_presidi,
    presidi_per_100k,
    posti_letto,
    posti_letto_per_100k,
    posti_letto_anziani,
    case
        when posti_letto is not null and posti_letto > 0
        then round(100.0 * posti_letto_anziani / posti_letto, 1)
    end as quota_posti_letto_anziani_pct,
    personale_retribuito,
    personale_volontario
from tot
order by anno, ref_area_codice
