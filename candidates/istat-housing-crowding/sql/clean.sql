-- clean.sql: crowding index 33_179
-- Canale dbnomics · macros toolkit (normalize_string / cast_int / cast_double)

select
    cast_int(TIME_PERIOD) as anno,
    normalize_string(REF_AREA) as ref_area_codice,
    case normalize_string(REF_AREA)
        when 'IT' then 'Italia'
        else normalize_string(REF_AREA)
    end as ref_area,
    normalize_string(DATA_TYPE) as indicatore_codice,
    'ABITAZ_AFFOLL_MED' as misura_codice,
    normalize_string(TENURE_STATUS) as titolo_godimento_codice,
    case normalize_string(TENURE_STATUS)
        when '1' then 'Proprietà'
        when '2' then 'Affitto'
        else normalize_string(TENURE_STATUS)
    end as titolo_godimento,
    cast_double(OBS_VALUE) as componenti_per_100mq
from raw_input
where cast_int(TIME_PERIOD) is not null
  and normalize_string(DATA_TYPE) = 'ABITAZ_AFFOLL_MED'
  and normalize_string(TENURE_STATUS) in ('1', '2')
  and cast_double(OBS_VALUE) is not null
