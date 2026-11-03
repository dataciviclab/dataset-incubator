-- clean.sql: trasporto ferroviario (ISTAT 117_1057 via DBnomics).
-- Molte dimensioni sono costanti per serie (ALL/WORLD): restano in chiaro e il
-- mart seleziona quelle che contano.

select
    cast_int(TIME_PERIOD) as anno,
    normalize_string(REF_AREA) as area,
    normalize_string(DATA_TYPE) as unita,
    normalize_string(GOODS_TRANSPORT_NST_2007) as merce_nst,
    normalize_string(INTERMODAL_TR_UNIT) as unita_carico,
    normalize_string(COUNTRY_GOOD_ORIGIN) as paese_origine,
    normalize_string(COUNTRY_GOOD_DESTINATION) as paese_destinazione,
    normalize_string(CATEG_TRANSPORT) as categoria_trasporto,
    cast_double(OBS_VALUE) as valore
from raw_input
where cast_double(OBS_VALUE) is not null
