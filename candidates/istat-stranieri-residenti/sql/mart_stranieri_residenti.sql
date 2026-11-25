-- mart_stranieri_residenti: stranieri residenti per anno x regione x
-- cittadinanza (solo paesi), con quota % sul totale della regione nell'anno.
--
-- Grano completo: `regione` (il livello `provincia` e' parziale nel dato).
with base as (
    select anno, territorio_codice, territorio, cittadinanza_codice, cittadinanza, residenti
    from clean_input
    where livello = 'regione' and not aggregato and residenti is not null
),
tot as (
    select anno, territorio_codice, sum(residenti) as totale_regione
    from base
    group by 1, 2
)
select
    b.anno,
    b.territorio_codice,
    b.territorio,
    b.cittadinanza_codice,
    b.cittadinanza,
    b.residenti,
    round(b.residenti / nullif(t.totale_regione, 0) * 100, 2) as quota_pct
from base b
join tot t on t.anno = b.anno and t.territorio_codice = b.territorio_codice
order by b.anno, b.territorio_codice, b.residenti desc
