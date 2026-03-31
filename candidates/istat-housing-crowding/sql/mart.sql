select
    anno,
    ref_area,
    titolo_godimento,
    componenti_per_100mq
from clean_input
order by anno, titolo_godimento
