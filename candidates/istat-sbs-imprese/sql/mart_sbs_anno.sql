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
        when 'E12150_PER_ADD_Q1' then 'va_per_addetto_q1'
        when 'E12150_PER_ADD_Q2' then 'va_per_addetto_q2'
        when 'E12150_PER_ADD_Q3' then 'va_per_addetto_q3'
        when 'E13310_PER_DIP_Q1' then 'costo_personale_dipendente_q1'
        when 'E13310_PER_DIP_Q2' then 'costo_personale_dipendente_q2'
        when 'E13310_PER_DIP_Q3' then 'costo_personale_dipendente_q3'
        when 'N00001_Q1' then 'wage_adjusted_labour_productivity_q1'
        when 'N00001_Q2' then 'wage_adjusted_labour_productivity_q2'
        when 'N00001_Q3' then 'wage_adjusted_labour_productivity_q3'
        else indicatore_codice
    end as indicatore_slug,
    coalesce(unita_misura, 'nd') as unita_misura
from clean_input
where size_class = 'Totale'
order by grain, territorio_codice, nace_codice, anno, indicatore_codice
