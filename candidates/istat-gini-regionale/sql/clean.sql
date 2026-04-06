select
    REF_AREA as regione,
    TIPO_DATO as tipo_dato,
    PRES_AFF_IMP as pres_aff_imp,
    TIME_PERIOD as anno,
    cast(OBS_VALUE as double) as gini
from raw_input
where TIPO_DATO = 'DISUG_REDDNET_GINI'
  and PRES_AFF_IMP in ('1', '2')
