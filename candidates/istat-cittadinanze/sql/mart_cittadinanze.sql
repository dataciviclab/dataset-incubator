-- mart_cittadinanze: acquisizioni di cittadinanza per anno x regione x
-- ex-cittadinanza (paesi), con quota % sul totale della regione.
--
-- Grano completo: `regione` (l'ex-cittadinanza non esiste a provincia).
-- Nota: nel dato la dimensione ex-cittadinanza compare SOLO con
-- processo='ALL' (il breakdown per processo non e' incrociato: vedi
-- mart_cittadinanze_processo).
with base as (
    select anno, territorio_codice, territorio,
           cittadinanza_codice, cittadinanza, acquisizioni
    from clean_input
    where livello = 'regione'
      and not aggregato
      and processo_codice = 'ALL'
      and acquisizioni is not null
),
tot as (
    select anno, territorio_codice, sum(acquisizioni) as totale_regione
    from base
    group by 1, 2
)
select
    b.anno,
    b.territorio_codice,
    b.territorio,
    b.cittadinanza_codice,
    b.cittadinanza,
    b.acquisizioni,
    round(b.acquisizioni / nullif(t.totale_regione, 0) * 100, 2) as quota_pct
from base b
join tot t on t.anno = b.anno and t.territorio_codice = b.territorio_codice
order by b.anno, b.territorio_codice, b.acquisizioni desc
