-- mart_italia_serie: serie nazionale per misura e anno (2019 e 2021)
-- Serve al controllo di coerenza e alla lettura del dato aggregato:
-- 2021: 35.271.829 abitazioni, 25.690.057 occupate, 9.581.772 non occupate (27,2%).
select
    anno,
    misura_codice,
    misura,
    cast(round(valore) as bigint) as valore
from clean_input
where livello_geografico = 'italia'
  and titolo_possesso_codice = 'ALL'
  and stanze_codice = 'TOT'
  and superficie_codice = 'ALL'
  and accessibilita_codice = 'TOTAL'
  and tipo_edificio_codice = 'TOTAL'
order by anno, misura_codice
