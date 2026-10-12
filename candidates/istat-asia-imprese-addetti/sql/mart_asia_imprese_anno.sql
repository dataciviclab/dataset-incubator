-- mart_asia_imprese_anno.sql

select
    anno,
    territorio_codice,
    territorio,
    livello,
    nace_codice,
    nace,
    indicatore_codice,
    indicatore,
    valore,
    case indicatore_codice
        when 'AENTN' then 'imprese'
        when 'AENTEMPDAA' then 'addetti'
        else indicatore_codice
    end as indicatore_slug,
    case when nace_codice = '0010' then 'totale' else 'sezione' end as livello_nace
from clean_input
order by livello, territorio_codice, livello_nace, nace_codice, anno, indicatore_codice
