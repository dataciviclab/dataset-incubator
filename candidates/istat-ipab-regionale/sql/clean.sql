select
    REF_AREA as area_codice,
    REF_AREA_label as area,
    case length(REF_AREA)
        when 2 then 'nazionale'
        when 3 then 'macro_area'
        when 4 then 'macro_area'
        when 5 then 'citta'
    end as livello_geografico,
    PURCHASES_DWELLINGS as tipo_abitazione,
    PURCHASES_DWELLINGS_label as tipo_abitazione_label,
    TIME_PERIOD as trimestre,
    cast(value as double) as indice_prezzi
from raw_input
where DATA_TYPE = '59'
  and MEASURE = '4'
  and TIME_PERIOD is not null
