-- mart_cittadinanze_processo: acquisizioni di cittadinanza per anno x regione
-- x processo di acquisizione (matrimonio / residenza / altro), con quota %.
--
-- Nel dato il processo compare con cittadinanza = WORLD (non e' incrociato
-- con l'ex-cittadinanza).
with base as (
    select anno, territorio_codice, territorio,
           processo_codice, processo, acquisizioni
    from clean_input
    where livello = 'regione'
      and cittadinanza_codice = 'WORLD'
      and processo_codice != 'ALL'
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
    b.processo_codice,
    b.processo,
    b.acquisizioni,
    round(b.acquisizioni / nullif(t.totale_regione, 0) * 100, 2) as quota_pct
from base b
join tot t on t.anno = b.anno and t.territorio_codice = b.territorio_codice
order by b.anno, b.territorio_codice, b.acquisizioni desc
