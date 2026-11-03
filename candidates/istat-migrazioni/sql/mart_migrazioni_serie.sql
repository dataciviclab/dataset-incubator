-- mart_migrazioni_serie: immigrazioni totali in Italia per anno (serie storica).
select
    anno,
    immigrazioni as immigrazioni_italia
from clean_input
where livello = 'nazionale' and immigrazioni is not null
order by anno
