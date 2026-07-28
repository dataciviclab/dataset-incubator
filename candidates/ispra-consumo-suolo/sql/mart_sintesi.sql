-- mart_sintesi — Consumo suolo: trend per livello (nazionale/regione/provincia)
--
-- Unisce i vecchi 3 trend separati in un unico mart con colonna `livello`.
-- Solo periodi annuali (2016-2024), non i pluriennali 2006-2012 e 2012-2015.

with
nazionale as (
    select
        'nazionale' as livello,
        'Italia' as entita,
        anno,
        count(*) as comuni,
        round(avg(stock_pct), 3) as avg_stock_pct,
        round(sum(stock_ha), 1) as tot_stock_ha,
        round(sum(incremento_netto_ha), 1) as tot_inc_netto_ha,
        round(sum(incremento_lordo_ha), 1) as tot_inc_lordo_ha,
        round(sum(ripristino_ha), 1) as tot_ripristino_ha
    from clean_input
    where periodo not in ('2006-2012', '2012-2015')
      and stock_ha is not null
    group by anno
),
regionale as (
    select
        'regione' as livello,
        regione as entita,
        anno,
        count(*) as comuni,
        round(avg(stock_pct), 3) as avg_stock_pct,
        round(sum(stock_ha), 1) as tot_stock_ha,
        round(sum(incremento_netto_ha), 1) as tot_inc_netto_ha,
        round(sum(incremento_lordo_ha), 1) as tot_inc_lordo_ha,
        round(sum(ripristino_ha), 1) as tot_ripristino_ha
    from clean_input
    where periodo not in ('2006-2012', '2012-2015')
      and stock_ha is not null
    group by regione, anno
),
provinciale as (
    select
        'provincia' as livello,
        provincia || ' (' || regione || ')' as entita,
        anno,
        count(*) as comuni,
        round(avg(stock_pct), 3) as avg_stock_pct,
        round(sum(stock_ha), 1) as tot_stock_ha,
        round(sum(incremento_netto_ha), 1) as tot_inc_netto_ha,
        round(sum(incremento_lordo_ha), 1) as tot_inc_lordo_ha,
        round(sum(ripristino_ha), 1) as tot_ripristino_ha
    from clean_input
    where periodo not in ('2006-2012', '2012-2015')
      and stock_ha is not null
      and provincia is not null
    group by regione, provincia, anno
)
select * from nazionale
union all
select * from regionale
union all
select * from provinciale
order by livello, entita, anno desc;
