select
    REF_AREA as regione_codice,
    REF_AREA_label as regione,
    DATA_TYPE as tipo_dato,
    IMPUTED_RENTS as pres_aff_imp,
    TIME_PERIOD as anno,
    cast_double(value) as gini
from raw_input
where DATA_TYPE = 'DISUG_REDDNET_GINI'
  and IMPUTED_RENTS in ('1', '2')
  and length(REF_AREA) = 4
