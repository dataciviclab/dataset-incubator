-- clean.sql: trasporto aereo (ISTAT 121_331 via DBnomics) — profilo.
select
    cast_int(TIME_PERIOD) as anno,
    normalize_string(AIRPORTS) as aeroporto,
    normalize_string(AIR_SERVICE_TYPE) as tipo_servizio,
    normalize_string(ARRIVING_DEPARTING) as arrivi_partenze,
    normalize_string(COUNTRY_PREV_NEXT) as paese,
    normalize_string(DATA_TYPE) as unita,
    cast_double(OBS_VALUE) as valore
from raw_input
where cast_double(OBS_VALUE) is not null
