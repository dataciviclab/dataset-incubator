-- mart_italia_serie: serie nazionale per misura e anno (2019, 2021, 2023)
-- Controllo di coerenza: 2021 = 35.271.829 abitazioni, 25.690.057 occupate,
-- 9.581.772 non occupate (27,2%).
select
    anno,
    misura_codice,
    misura,
    cast(round(valore) as bigint) as valore,
    case when anno = 2021 then 'enumerazione' else 'campione' end as tipo_rilevazione
from clean_input
where livello_geografico = 'italia'
  and titolo_possesso_codice = 'ALL'
order by anno, misura_codice
