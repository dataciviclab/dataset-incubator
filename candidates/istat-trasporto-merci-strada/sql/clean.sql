-- clean.sql: trasporto merci su strada (ISTAT 121_330 via DBnomics).
-- Grano: anno x regione di carico x regione di scarico x merceologia x tipo.
-- Le dimensioni restano in chiaro; la normalizzazione dei codici si fa nel mart.

select
    cast_int(TIME_PERIOD)          as anno,
    normalize_string(REG_LOADING)  as regione_carico,
    normalize_string(REG_UNLOADING) as regione_scarico,
    normalize_string(GOODS_TRANSPORT_NST_2007) as merce_nst,
    normalize_string(TITLE_OF_TRANSPORT)       as tipo_trasporto,
    normalize_string(DATA_TYPE)    as unita,
    normalize_string(DISTANCE_CLASS) as classe_distanza,
    cast_double(OBS_VALUE)         as valore
from raw_input
where cast_double(OBS_VALUE) is not null
