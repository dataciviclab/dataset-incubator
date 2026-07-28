-- mart_trend — IRPEF Comunale: trend e CAGR reddituale
--
-- Legge TUTTI gli anni dal clean via glob (multi-anno).
-- Rimpiazza il vecchio irpef_capacita_fiscale_multi_anno con CAGR
-- e delta su tutta la serie disponibile.
--
-- Output: 1 riga = 1 comune/regione × trend.
-- Due livelli: comune (dettaglio) + regione (sintesi).

with
all_clean as (
    select
        anno_di_imposta, codice_istat_comune, denominazione_comune,
        sigla_provincia, regione,
        numero_contribuenti, reddito_imponibile_eur,
        imposta_netta_eur, addizionale_comunale_dovuta_eur
    from read_parquet(
        '{root}/data/clean/{dataset}/*/{dataset}_*_clean.parquet',
        union_by_name=true
    )
    where codice_istat_comune is not null
      and regione is not null
      and numero_contribuenti > 0
      and reddito_imponibile_eur > 0
),
-- Serie comunale
comuni_anno as (
    select
        anno_di_imposta as anno,
        codice_istat_comune,
        denominazione_comune,
        regione,
        sigla_provincia,
        sum(numero_contribuenti) as contribuenti,
        sum(reddito_imponibile_eur) as reddito_totale,
        sum(imposta_netta_eur) as imposta_totale,
        sum(addizionale_comunale_dovuta_eur) as addizionale_totale
    from all_clean
    group by anno, codice_istat_comune, denominazione_comune, regione, sigla_provincia
),
-- Serie regionale
regioni_anno as (
    select
        anno_di_imposta as anno,
        regione,
        sum(numero_contribuenti) as contribuenti,
        sum(reddito_imponibile_eur) as reddito_totale,
        sum(imposta_netta_eur) as imposta_totale,
        sum(addizionale_comunale_dovuta_eur) as addizionale_totale
    from all_clean
    group by anno, regione
),
-- Trend comuni
trend_comuni as (
    select
        'comune' as livello,
        codice_istat_comune || ' - ' || denominazione_comune || ' (' || sigla_provincia || ')' as entita,
        min(anno) as primo_anno,
        max(anno) as ultimo_anno,
        count(*) as anni_coperti,
        min(contribuenti) as contribuenti,
        min(reddito_totale) filter (where anno = (select min(a2.anno) from comuni_anno a2 where a2.codice_istat_comune = c.codice_istat_comune)) as reddito_iniziale,
        max(reddito_totale) filter (where anno = (select max(a2.anno) from comuni_anno a2 where a2.codice_istat_comune = c.codice_istat_comune)) as reddito_finale,
        round(
            max(reddito_totale) filter (where anno = (select max(a2.anno) from comuni_anno a2 where a2.codice_istat_comune = c.codice_istat_comune))
            - min(reddito_totale) filter (where anno = (select min(a2.anno) from comuni_anno a2 where a2.codice_istat_comune = c.codice_istat_comune))
        , 0) as delta_reddito_eur,
        case
            when min(reddito_totale) filter (where anno = (select min(a2.anno) from comuni_anno a2 where a2.codice_istat_comune = c.codice_istat_comune)) > 0
                 and max(anno) > min(anno)
            then round((power(
                max(reddito_totale) filter (where anno = (select max(a2.anno) from comuni_anno a2 where a2.codice_istat_comune = c.codice_istat_comune))
                / nullif(min(reddito_totale) filter (where anno = (select min(a2.anno) from comuni_anno a2 where a2.codice_istat_comune = c.codice_istat_comune)), 0),
                1.0 / (max(anno) - min(anno))
            ) - 1) * 100, 2)
        end as cagr_reddito_pct
    from comuni_anno c
    group by codice_istat_comune, denominazione_comune, sigla_provincia
),
-- Trend regioni
trend_regioni as (
    select
        'regione' as livello,
        regione as entita,
        min(anno) as primo_anno,
        max(anno) as ultimo_anno,
        count(*) as anni_coperti,
        min(reddito_totale) filter (where anno = (select min(a2.anno) from regioni_anno a2 where a2.regione = r.regione)) as reddito_iniziale,
        max(reddito_totale) filter (where anno = (select max(a2.anno) from regioni_anno a2 where a2.regione = r.regione)) as reddito_finale,
        round(
            max(reddito_totale) filter (where anno = (select max(a2.anno) from regioni_anno a2 where a2.regione = r.regione))
            - min(reddito_totale) filter (where anno = (select min(a2.anno) from regioni_anno a2 where a2.regione = r.regione))
        , 0) as delta_reddito_eur,
        case
            when min(reddito_totale) filter (where anno = (select min(a2.anno) from regioni_anno a2 where a2.regione = r.regione)) > 0
                 and max(anno) > min(anno)
            then round((power(
                max(reddito_totale) filter (where anno = (select max(a2.anno) from regioni_anno a2 where a2.regione = r.regione))
                / nullif(min(reddito_totale) filter (where anno = (select min(a2.anno) from regioni_anno a2 where a2.regione = r.regione)), 0),
                1.0 / (max(anno) - min(anno))
            ) - 1) * 100, 2)
        end as cagr_reddito_pct
    from regioni_anno r
    group by regione
)
select
    livello,
    entita,
    primo_anno,
    ultimo_anno,
    anni_coperti,
    delta_reddito_eur,
    cagr_reddito_pct,
    case
        when cagr_reddito_pct is null then null
        when cagr_reddito_pct > 5.0 then 'CRESCITA_FORTE'
        when cagr_reddito_pct > 2.0 then 'CRESCITA_MODERATA'
        when cagr_reddito_pct > -2.0 then 'STABILE'
        when cagr_reddito_pct > -5.0 then 'CALO_MODERATO'
        else 'CALO_FORTE'
    end as segnale_trend_reddito
from trend_comuni
union all
select
    livello, entita, primo_anno, ultimo_anno, anni_coperti,
    delta_reddito_eur, cagr_reddito_pct,
    case
        when cagr_reddito_pct is null then null
        when cagr_reddito_pct > 5.0 then 'CRESCITA_FORTE'
        when cagr_reddito_pct > 2.0 then 'CRESCITA_MODERATA'
        when cagr_reddito_pct > -2.0 then 'STABILE'
        when cagr_reddito_pct > -5.0 then 'CALO_MODERATO'
        else 'CALO_FORTE'
    end as segnale_trend_reddito
from trend_regioni
order by livello, delta_reddito_eur desc nulls last;
