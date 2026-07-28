-- mart_trend — ISPRA Rifiuti Urbani: trend e dinamiche temporali
--
-- Legge TUTTI gli anni dal clean (via {root}/data/clean/*/*.parquet)
-- perché il trend (CAGR, delta, pendenza) richiede multi-anno.
-- Singolo anno produrrebbe CAGR NULL.
--
-- Output: 1 riga = 1 provincia/regione con metriche di trend.
-- Due livelli: provincia (dettaglio) + regione (sintesi).
--
-- NOTA: usa {root} e {dataset} che il toolkit sostituisce automaticamente.

with
-- Legge TUTTI gli anni del dataset con un glob sul clean parquet
all_clean as (
    select
        anno, codice_comune_istat, regione, provincia, comune,
        popolazione, totale_ru_tonnellate, totale_rd_tonnellate, percentuale_rd
    from read_parquet(
        '{root}/data/clean/{dataset}/*/{dataset}_*_clean.parquet',
        union_by_name=true
    )
    where popolazione > 0
),
-- 1. Serie provinciale: RD% medio pesato per provincia × anno
province_anno as (
    select
        anno,
        regione,
        provincia,
        round(sum(percentuale_rd * popolazione) / nullif(sum(popolazione), 0), 2) as rd_medio,
        round(sum(totale_ru_tonnellate * 1000.0) / nullif(sum(popolazione), 0), 1) as kg_ru_procapite,
        round(sum(totale_rd_tonnellate * 1000.0) / nullif(sum(popolazione), 0), 1) as kg_rd_procapite
    from all_clean
    where provincia is not null
    group by anno, regione, provincia
),
-- 2. Serie regionale (stessa logica, aggregata a regione)
regioni_anno as (
    select
        anno,
        regione,
        round(sum(percentuale_rd * popolazione) / nullif(sum(popolazione), 0), 2) as rd_medio,
        round(sum(totale_ru_tonnellate * 1000.0) / nullif(sum(popolazione), 0), 1) as kg_ru_procapite,
        round(sum(totale_rd_tonnellate * 1000.0) / nullif(sum(popolazione), 0), 1) as kg_rd_procapite
    from all_clean
    where regione is not null
    group by anno, regione
),
-- 3. Trend province: CAGR, delta, primo/ultimo anno
trend_province as (
    select
        'provincia' as livello,
        provincia || ' (' || regione || ')' as entita,
        min(anno) as primo_anno,
        max(anno) as ultimo_anno,
        count(*) as anni_coperti,
        -- Primo e ultimo valore (usando first/last per semplicità)
        min(rd_medio) filter (where anno = (select min(a2.anno) from province_anno a2 where a2.provincia = p.provincia and a2.regione = p.regione)) as rd_iniziale,
        max(rd_medio) filter (where anno = (select max(a2.anno) from province_anno a2 where a2.provincia = p.provincia and a2.regione = p.regione)) as rd_finale,
        round(
            max(rd_medio) filter (where anno = (select max(a2.anno) from province_anno a2 where a2.provincia = p.provincia and a2.regione = p.regione))
            - min(rd_medio) filter (where anno = (select min(a2.anno) from province_anno a2 where a2.provincia = p.provincia and a2.regione = p.regione))
        , 2) as delta_rd_punti,
        -- CAGR: (val_fine/val_inizio)^(1/anni) - 1
        case
            when min(rd_medio) filter (where anno = (select min(a2.anno) from province_anno a2 where a2.provincia = p.provincia and a2.regione = p.regione)) > 0
                 and max(anno) > min(anno)
            then round((power(
                max(rd_medio) filter (where anno = (select max(a2.anno) from province_anno a2 where a2.provincia = p.provincia and a2.regione = p.regione))
                / nullif(min(rd_medio) filter (where anno = (select min(a2.anno) from province_anno a2 where a2.provincia = p.provincia and a2.regione = p.regione)), 0),
                1.0 / (max(anno) - min(anno))
            ) - 1) * 100, 2)
        end as cagr_rd_pct,
        -- Pendenza (coefficiente angolare RD ~ anno)
        round(
            (count(*) * sum(anno * rd_medio) - sum(anno) * sum(rd_medio))
            / nullif(count(*) * sum(anno * anno) - sum(anno) * sum(anno), 0)
        , 2) as pendenza_annua_rd,
        -- var_media_annua richiederebbe avg(lag) in subquery — omessa per semplicità
    from province_anno p
    group by regione, provincia
),
-- 4. Trend regioni (stessa logica)
trend_regioni as (
    select
        'regione' as livello,
        regione as entita,
        min(anno) as primo_anno,
        max(anno) as ultimo_anno,
        count(*) as anni_coperti,
        min(rd_medio) filter (where anno = (select min(a2.anno) from regioni_anno a2 where a2.regione = r.regione)) as rd_iniziale,
        max(rd_medio) filter (where anno = (select max(a2.anno) from regioni_anno a2 where a2.regione = r.regione)) as rd_finale,
        round(
            max(rd_medio) filter (where anno = (select max(a2.anno) from regioni_anno a2 where a2.regione = r.regione))
            - min(rd_medio) filter (where anno = (select min(a2.anno) from regioni_anno a2 where a2.regione = r.regione))
        , 2) as delta_rd_punti,
        case
            when min(rd_medio) filter (where anno = (select min(a2.anno) from regioni_anno a2 where a2.regione = r.regione)) > 0
                 and max(anno) > min(anno)
            then round((power(
                max(rd_medio) filter (where anno = (select max(a2.anno) from regioni_anno a2 where a2.regione = r.regione))
                / nullif(min(rd_medio) filter (where anno = (select min(a2.anno) from regioni_anno a2 where a2.regione = r.regione)), 0),
                1.0 / (max(anno) - min(anno))
            ) - 1) * 100, 2)
        end as cagr_rd_pct,
        round(
            (count(*) * sum(anno * rd_medio) - sum(anno) * sum(rd_medio))
            / nullif(count(*) * sum(anno * anno) - sum(anno) * sum(anno), 0)
        , 2) as pendenza_annua_rd
    from regioni_anno r
    group by regione
),
-- 5. Unione
tutti_trend as (
    select * from trend_province
    union all
    select * from trend_regioni
)
select
    livello,
    entita,
    primo_anno,
    ultimo_anno,
    anni_coperti,
    round(rd_iniziale, 2) as rd_iniziale,
    round(rd_finale, 2) as rd_finale,
    delta_rd_punti,
    cagr_rd_pct,
    pendenza_annua_rd,
    -- Segnale di tendenza
    case
        when cagr_rd_pct is null then null
        when cagr_rd_pct > 2.0 then 'CRESCITA_FORTE'
        when cagr_rd_pct > 0.5 then 'CRESCITA_MODERATA'
        when cagr_rd_pct > -0.5 then 'STABILE'
        when cagr_rd_pct > -2.0 then 'CALO_MODERATO'
        else 'CALO_FORTE'
    end as segnale_trend_rd
from tutti_trend
order by livello, abs(coalesce(delta_rd_punti, 0)) desc;
