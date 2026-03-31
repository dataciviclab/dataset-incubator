select
    try_cast(TIME_PERIOD as integer) as anno,
    REF_AREA as ref_area_codice,
    REF_AREA_label as ref_area,
    TENURE_STATUS as titolo_godimento_codice,
    TENURE_STATUS_label as titolo_godimento,
    DATA_TYPE as indicatore_codice,
    DATA_TYPE_label as indicatore,
    MEASURE as misura_codice,
    MEASURE_label as misura,
    try_cast(value as double) as componenti_per_100mq
from raw_input
where try_cast(TIME_PERIOD as integer) is not null
