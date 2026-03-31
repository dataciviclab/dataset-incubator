select
    anno,
    ref_area,
    titolo_godimento,
    componenti_per_100mq
from clean_input
where anno >= 2004
order by anno, titolo_godimento
