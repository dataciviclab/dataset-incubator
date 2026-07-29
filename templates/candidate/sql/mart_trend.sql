-- mart_trend — trend, CAGR e dinamiche temporali
--
-- ATTIVARE SOLO se la serie storica copre 5+ anni.
-- Livello di aggregazione: PROVINCIA / REGIONE (non comune —
-- troppe righe, beneficio marginale, costo alto).
--
-- Output: 1 riga = (provincia/regione × metrica × trend)
-- Il formato è "long": ogni indicatore di trend è una colonna.
--
-- Personalizzazione:
--   1. Sostituisci {livello} con provincia oppure regione
--   2. Sostituisci {colonna_livello} con il nome della colonna nel clean
--      (es. sigla_provincia, provincia, regione)
--   3. Sostituisci {metrica} con la colonna numerica da trendare
--   4. Se il dataset ha più metriche, duplica la sezione trend
--   5. Se {colonna_livello} non esiste nel clean (es. dataset regionale
--      ma colonna "regione" già presente), togli la GROUP BY livello
--      e lascia solo anno.
--   6. Regola anno_min per il calcolo del CAGR (primo anno disponibile).

with
-- Parametri: finestra temporale
param as (
    select
        min(anno) as anno_inizio,
        max(anno) as anno_fine,
        max(anno) - min(anno) as anni_delta
    from clean_input
    where {metrica} is not null
),
-- Aggregazione per livello × anno
serie as (
    select
        {colonna_livello} as livello,
        anno,
        count(*)                                       as n_osservazioni,
        sum({metrica})                                 as valore_totale,
        avg({metrica})                                 as valore_medio,
        -- Per CAGR serve valore aggregato per anno
    from clean_input
    where {metrica} is not null
    group by {colonna_livello}, anno
),
-- Trend per livello
trend as (
    select
        livello,
        min(anno)                                      as primo_anno,
        max(anno)                                      as ultimo_anno,
        count(*)                                       as anni_coperti,
        -- Valore primo e ultimo anno
        max(case when anno = (select anno_inizio from param)
                 then valore_totale end)                as valore_iniziale,
        max(case when anno = (select anno_fine from param)
                 then valore_totale end)                as valore_finale,
        -- Delta assoluto (ultimo - primo)
        max(case when anno = (select anno_fine from param)
                 then valore_totale end)
        - max(case when anno = (select anno_inizio from param)
                   then valore_totale end)              as delta_assoluto,
        -- Variazione percentuale totale
        case
            when max(case when anno = (select anno_inizio from param)
                          then valore_totale end) <> 0
            then (max(case when anno = (select anno_fine from param)
                           then valore_totale end)
                  - max(case when anno = (select anno_inizio from param)
                             then valore_totale end))
                 / abs(max(case when anno = (select anno_inizio from param)
                                then valore_totale end)) * 100
        end as delta_percentuale_totale,
        -- CAGR (tasso di crescita annuale composto)
        -- Formula: (val_fine / val_inizio)^(1/anni) - 1
        case
            when max(case when anno = (select anno_inizio from param)
                          then valore_totale end) > 0
                 and (select anni_delta from param) > 0
            then pow(
                max(case when anno = (select anno_fine from param)
                         then valore_totale end)
                / max(case when anno = (select anno_inizio from param)
                           then valore_totale end),
                1.0 / (select anni_delta from param)
            ) - 1
        end as cagr,
        -- Media del periodo
        avg(valore_totale)                              as media_periodo,
        -- Anno con valore massimo e minimo
        max(valore_totale)                              as picco_massimo,
        min(valore_totale)                              as valle_minimo
    from serie
    group by livello
),
-- Variazioni anno su anno (per vedere trend recenti)
variazioni_aa as (
    select
        livello,
        anno,
        valore_totale,
        valore_medio,
        -- Variazione % sull'anno precedente (per singolo livello)
        (valore_totale - lag(valore_totale) over (
            partition by livello order by anno
        )) / nullif(lag(valore_totale) over (
            partition by livello order by anno
        ), 0) * 100 as var_pct_aa,
        -- Variazione % media mobile 3 anni (se abbastanza anni)
        avg(valore_totale) over (
            partition by livello
            order by anno
            rows between 2 preceding and current row
        ) as media_mobile_3aa
    from serie
)
select
    t.*,
    -- Segnale di tendenza
    case
        when t.cagr is null then null
        when t.cagr > 0.05 then 'CRESCITA_FORTE'
        when t.cagr > 0.01 then 'CRESCITA_MODERATA'
        when t.cagr > -0.01 then 'STABILE'
        when t.cagr > -0.05 then 'CALO_MODERATO'
        else 'CALO_FORTE'
    end as segnale_trend,
    -- Ultima variazione anno su anno disponibile
    v.var_pct_aa as var_pct_aa_anno_fine,
    v.media_mobile_3aa
from trend t
left join variazioni_aa v
    on t.livello = v.livello
    and t.ultimo_anno = v.anno
order by t.livello;
