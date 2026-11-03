-- clean.sql: trasporto marittimo (ISTAT 121_393 via DBnomics) — profilo.
select
    cast_int(TIME_PERIOD) as anno,
    normalize_string(MAR_REG_UNLOADING) as regione_sbarco,
    normalize_string(MAR_REG_LOADING) as regione_carico,
    normalize_string(GOODS_TRANSPORT_NST_2007) as merce_nst,
    normalize_string(DATA_TYPE) as unita,
    cast_double(OBS_VALUE) as valore
from raw_input
where cast_double(OBS_VALUE) is not null
