-- mart_permessi: permessi di soggiorno validi per anno x regione x cittadinanza
-- (solo paesi), con quota % sul totale della regione nell'anno.
--
-- Grano completo: `regione` (il livello `provincia` e' parziale nel dato).
-- Esclude gli aggregati (territori macro + aree geopolitiche/WORLD).

with base as (
    select anno, territorio_codice, territorio, cittadinanza_codice, cittadinanza, permessi
    from clean_input
    where livello = 'regione' and not aggregato and permessi is not null
),
tot as (
    select anno, territorio_codice, sum(permessi) as totale_regione
    from base
    group by 1, 2
)
select
    b.anno,
    b.territorio_codice,
    b.territorio,
    b.cittadinanza_codice,
    b.cittadinanza,
    b.permessi,
    round(b.permessi / nullif(t.totale_regione, 0) * 100, 2) as quota_pct
from base b
join tot t on t.anno = b.anno and t.territorio_codice = b.territorio_codice
order by b.anno, b.territorio_codice, b.permessi desc
