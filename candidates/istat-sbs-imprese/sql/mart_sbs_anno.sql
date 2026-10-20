-- mart_sbs_anno.sql
-- valore: unità originali (mila_eur o conte) — vedi unita_misura

select
    anno,
    territorio_codice,
    territorio,
    grain,
    case grain
        when 'nazionale' then 'italia'
        when 'regionale' then 'nuts1'
        else grain
    end as livello,
    nace_codice,
    nace,
    indicatore_codice,
    indicatore,
    valore,
    case indicatore_codice
        when '12110' then 'fatturato'
        when '12120' then 'valore_produzione'
        when '12150' then 'valore_aggiunto'
        when '12170' then 'risultato_lordo_gestione'
        when '13310' then 'costi_personale'
        when '13320' then 'salari_stipendi'
        when '13330' then 'contributi_sociali'
        when '15110' then 'investimenti_fissi_lordi'
        when '16150' then 'ore_lavorate'
        when '11110' then 'imprese'
        when '11210' then 'unita_locali'
        else indicatore_codice
    end as indicatore_slug,
    coalesce(unita_misura, 'nd') as unita_misura
from clean_input
order by grain, territorio_codice, nace_codice, anno, indicatore_codice
