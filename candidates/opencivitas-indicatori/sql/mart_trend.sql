-- mart_trend — OpenCivitas: trend indicatori per comune su 7 anni
--
-- Legge TUTTI gli anni dal clean via glob.
-- Per ogni (comune, ambito, indicatore): CAGR, delta, primo/ultimo anno.
-- ~280 indicatori × ~7.000 comuni = ~2M righe di trend.

with all_clean as (
    select anno, username, ambito, indicatore, valore_num
    from read_parquet(
        '{root}/data/clean/{dataset}/*/{dataset}_*_clean.parquet',
        union_by_name=true
    )
    where valore_num is not null
      and tipo_indicatore in ('IND', 'DET')
),
serie as (
    select
        username,
        ambito,
        indicatore,
        anno,
        avg(valore_num) as valore_medio
    from all_clean
    group by username, ambito, indicatore, anno
),
trend as (
    select
        username,
        ambito,
        indicatore,
        min(anno) as primo_anno,
        max(anno) as ultimo_anno,
        count(*) as anni_coperti,
        min(valore_medio) filter (where anno = (select min(a2.anno) from serie a2 where a2.username = s.username and a2.ambito = s.ambito and a2.indicatore = s.indicatore)) as valore_iniziale,
        max(valore_medio) filter (where anno = (select max(a2.anno) from serie a2 where a2.username = s.username and a2.ambito = s.ambito and a2.indicatore = s.indicatore)) as valore_finale,
        round(
            max(valore_medio) filter (where anno = (select max(a2.anno) from serie a2 where a2.username = s.username and a2.ambito = s.ambito and a2.indicatore = s.indicatore))
            - min(valore_medio) filter (where anno = (select min(a2.anno) from serie a2 where a2.username = s.username and a2.ambito = s.ambito and a2.indicatore = s.indicatore))
        , 4) as delta_assoluto,
        case
            when min(valore_medio) filter (where anno = (select min(a2.anno) from serie a2 where a2.username = s.username and a2.ambito = s.ambito and a2.indicatore = s.indicatore)) > 0
                 and max(anno) > min(anno)
            then round((power(
                max(valore_medio) filter (where anno = (select max(a2.anno) from serie a2 where a2.username = s.username and a2.ambito = s.ambito and a2.indicatore = s.indicatore))
                / nullif(min(valore_medio) filter (where anno = (select min(a2.anno) from serie a2 where a2.username = s.username and a2.ambito = s.ambito and a2.indicatore = s.indicatore)), 0),
                1.0 / (max(anno) - min(anno))
            ) - 1) * 100, 2)
        end as cagr_pct
    from serie s
    group by username, ambito, indicatore
)
select
    username,
    ambito,
    indicatore,
    primo_anno,
    ultimo_anno,
    anni_coperti,
    round(valore_iniziale, 4) as valore_iniziale,
    round(valore_finale, 4) as valore_finale,
    delta_assoluto,
    cagr_pct,
    case
        when cagr_pct is null then null
        when cagr_pct > 10 then 'CRESCITA_FORTE'
        when cagr_pct > 3 then 'CRESCITA_MODERATA'
        when cagr_pct > -3 then 'STABILE'
        when cagr_pct > -10 then 'CALO_MODERATO'
        else 'CALO_FORTE'
    end as segnale_trend
from trend
order by abs(coalesce(cagr_pct, 0)) desc;
