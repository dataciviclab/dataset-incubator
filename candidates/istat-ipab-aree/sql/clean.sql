-- clean.sql: IPAB aree 143_497
-- Canale dbnomics · macros toolkit (normalize_string / cast_double)

select
    normalize_string(REF_AREA) as area_codice,
    case normalize_string(REF_AREA)
        when 'IT' then 'Italia'
        else normalize_string(REF_AREA)
    end as area,
    case length(normalize_string(REF_AREA))
        when 2 then 'nazionale'
        when 3 then 'macro_area'
        when 4 then 'macro_area'
        when 5 then 'citta'
        else 'altro'
    end as livello_geografico,
    normalize_string(PURCHASES_DWELLINGS) as tipo_abitazione,
    case normalize_string(PURCHASES_DWELLINGS)
        when 'NEW_DW' then 'Nuove costruzioni'
        when 'EXST_DW' then 'Abitazioni esistenti'
        else normalize_string(PURCHASES_DWELLINGS)
    end as tipo_abitazione_label,
    normalize_string(TIME_PERIOD) as trimestre,
    cast_double(OBS_VALUE) as indice_prezzi
from raw_input
where normalize_string(DATA_TYPE) = '59'
  and normalize_string(MEASURE) = '4'
  and normalize_string(TIME_PERIOD) is not null
  and cast_double(OBS_VALUE) is not null
