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
        when '12150' then 'valore_aggiunto'
        when '12120' then 'valore_produzione'
        when '13310' then 'costi_personale'
        when '11210' then 'unita_locali'
        else indicatore_codice
    end as indicatore_slug,
    coalesce(unita_misura, 'nd') as unita_misura
from clean_input
order by grain, territorio_codice, nace_codice, anno, indicatore_codice
