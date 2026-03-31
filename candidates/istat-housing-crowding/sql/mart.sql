select
    anno,
    ref_area,
    titolo_godimento,
    componenti_per_100mq
from clean_input
where ref_area_codice = 'IT'
  and titolo_godimento_codice in ('1', '2')
order by anno, titolo_godimento
