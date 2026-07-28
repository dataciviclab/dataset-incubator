-- mart_comuni — Consumo suolo: arricchimento + benchmark comunale
--
-- Stessa cardinalità del clean (1 riga = 1 comune × periodo).
-- Aggiunge benchmark su stock_pct e incremento_netto_ha.

with base as (
    select
        pro_com,
        comune,
        provincia,
        regione,
        periodo,
        anno,
        incremento_netto_ha,
        incremento_lordo_ha,
        ripristino_ha,
        stock_ha,
        stock_pct,
        -- Classe di consumo suolo (basata su stock_pct)
        case
            when stock_pct < 5.0  then 'A_MENO_5'
            when stock_pct < 10.0 then 'B_5_10'
            when stock_pct < 20.0 then 'C_10_20'
            when stock_pct < 30.0 then 'D_20_30'
            else                       'E_OLTRE_30'
        end as classe_consumo
    from clean_input
    where pro_com is not null
      and stock_ha is not null
)
select
    *,
    -- Benchmark stock_pct: media nazionale e regionale per periodo
    round(avg(stock_pct) over (partition by periodo), 4) as media_nazionale_stock_pct,
    round(avg(stock_pct) over (partition by periodo, regione), 4) as media_regionale_stock_pct,
    round(stddev(stock_pct) over (partition by periodo), 4) as std_nazionale_stock_pct,
    case
        when stock_pct is null then null
        else round(percent_rank() over (partition by periodo order by stock_pct), 4)
    end as percentile_stock_pct,
    -- Distanza % dalla media nazionale
    case
        when avg(stock_pct) over (partition by periodo) <> 0
        then round((stock_pct - avg(stock_pct) over (partition by periodo))
             / abs(avg(stock_pct) over (partition by periodo)) * 100, 2)
    end as distanza_media_nazionale_pct,
    -- Benchmark incremento netto
    round(avg(incremento_netto_ha) over (partition by periodo), 4) as media_nazionale_inc_netto,
    round(avg(incremento_netto_ha) over (partition by periodo, regione), 4) as media_regionale_inc_netto,
    case
        when incremento_netto_ha is null then null
        else round(percent_rank() over (partition by periodo order by incremento_netto_ha), 4)
    end as percentile_inc_netto,
    -- Fascia stock_pct
    case
        when stock_pct is null then null
        when percent_rank() over (partition by periodo order by stock_pct) >= 0.8 then 'ELEVATO'
        when percent_rank() over (partition by periodo order by stock_pct) >= 0.6 then 'SOPRA_MEDIA'
        when percent_rank() over (partition by periodo order by stock_pct) >= 0.4 then 'MEDIA'
        when percent_rank() over (partition by periodo order by stock_pct) >= 0.2 then 'SOTTO_MEDIA'
        else 'BASSO'
    end as fascia_consumo_suolo
from base
order by pro_com, anno desc;
