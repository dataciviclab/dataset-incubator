-- mart_migrazioni: immigrazioni (dall'estero) per anno x regione, con quota %
-- sul totale Italia dell'anno.
--
-- Grano completo: `regione` (il livello `provincia` e' parziale nel dato).
with base as (
    select anno, territorio_codice, territorio, immigrazioni
    from clean_input
    where livello = 'regione' and not aggregato and immigrazioni is not null
),
tot as (
    select anno, sum(immigrazioni) as totale_italia
    from base
    group by 1
)
select
    b.anno,
    b.territorio_codice,
    b.territorio,
    b.immigrazioni,
    round(b.immigrazioni / nullif(t.totale_italia, 0) * 100, 2) as quota_pct
from base b
join tot t on t.anno = b.anno
order by b.anno, b.immigrazioni desc
