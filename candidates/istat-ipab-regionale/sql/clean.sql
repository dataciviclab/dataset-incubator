select
    REF_AREA as regione_codice,
    REF_AREA_label as regione,
    ABIT_COMPRAV as tipo_abitazione,
    ABIT_COMPRAV_label as tipo_abitazione_label,
    TIME_PERIOD as trimestre,
    cast(value as double) as indice_prezzi
from raw_input
where IND_TYPE = '59'
  and MISURA1 = '4'
  and length(REF_AREA) = 4
  and TIME_PERIOD is not null
