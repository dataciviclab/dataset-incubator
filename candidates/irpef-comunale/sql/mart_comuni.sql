-- mart_comuni — IRPEF Comunale: arricchimento + benchmark reddituale
--
-- Unisce i vecchi: irpef_by_comune + mart_pressione_fiscale + benchmark.
-- Stessa cardinalità del clean (1 riga = 1 comune × anno).
--
-- Novità rispetto ai vecchi mart:
--   • Reddito pro-capite (join con popolazione)
--   • Benchmark: media nazionale/regionale, percentile, fascia per reddito medio e pro-capite
--   • Rank regionale per reddito e aliquota
--
-- NOTA: la popolazione è letta dal support dataset o via glob.
-- Se il support non è disponibile, le colonne pro-capite saranno NULL.

with
popolazione as (
    select codice_comune, anno, sum(popolazione_residente) as residenti
    from read_parquet(
        '{root}/data/clean/popolazione_istat_comunale_2019_2025/*/*_clean.parquet',
        union_by_name=true
    )
    group by codice_comune, anno
),
base as (
    select
        c.anno_di_imposta as anno,
        c.codice_istat_comune,
        c.denominazione_comune,
        c.sigla_provincia,
        c.regione,
        c.numero_contribuenti,
        c.reddito_imponibile_eur,
        c.imposta_netta_eur,
        c.addizionale_comunale_dovuta_eur,
        c.addizionale_regionale_dovuta_eur,
        c.reddito_da_lavoro_dipendente_e_assimilati_eur,
        c.reddito_da_pensione_eur,
        c.reddito_da_fabbricati_eur,
        c.reddito_da_partecipazione_eur,
        c.reddito_da_lavoro_autonomo_comprensivo_valori_nulli_eur,
        c.reddito_complessivo_eur,
        p.residenti as popolazione_residente,
        -- Reddito medio per contribuente
        c.reddito_imponibile_eur / nullif(c.numero_contribuenti, 0) as reddito_medio_per_contribuente,
        -- Reddito pro-capite (su popolazione residente, non solo contribuenti)
        c.reddito_imponibile_eur / nullif(p.residenti, 0) as reddito_procapite,
        -- Aliquota effettiva (imposta netta / reddito imponibile)
        c.imposta_netta_eur * 100.0 / nullif(c.reddito_imponibile_eur, 0) as aliquota_effettiva_pct,
        -- Addizionale comunale effettiva
        c.addizionale_comunale_dovuta_eur * 100.0 / nullif(c.reddito_imponibile_eur, 0) as addizionale_effettiva_pct
    from clean_input c
    left join popolazione p
        on c.codice_istat_comune = p.codice_comune
        and c.anno_di_imposta = p.anno
    where c.codice_istat_comune is not null
      and c.regione is not null
      and c.numero_contribuenti > 0
      and c.reddito_imponibile_eur > 0
)
select
    *,
    -- ================================================================
    -- BENCHMARK REDDITO MEDIO PER CONTRIBUENTE
    -- ================================================================
    round(avg(reddito_medio_per_contribuente) over (partition by anno), 0) as media_nazionale_reddito,
    round(avg(reddito_medio_per_contribuente) over (partition by anno, regione), 0) as media_regionale_reddito,
    round(stddev(reddito_medio_per_contribuente) over (partition by anno), 0) as std_nazionale_reddito,
    case
        when reddito_medio_per_contribuente is null then null
        else round(percent_rank() over (partition by anno order by reddito_medio_per_contribuente), 4)
    end as percentile_nazionale_reddito,
    -- Distanza % dalla media nazionale
    case
        when avg(reddito_medio_per_contribuente) over (partition by anno) <> 0
        then round((reddito_medio_per_contribuente - avg(reddito_medio_per_contribuente) over (partition by anno))
             / abs(avg(reddito_medio_per_contribuente) over (partition by anno)) * 100, 2)
    end as distanza_media_nazionale_pct,
    -- ================================================================
    -- BENCHMARK REDDITO PRO-CAPITE
    -- ================================================================
    round(avg(reddito_procapite) over (partition by anno), 0) as media_nazionale_procapite,
    round(avg(reddito_procapite) over (partition by anno, regione), 0) as media_regionale_procapite,
    case
        when reddito_procapite is null then null
        else round(percent_rank() over (partition by anno order by reddito_procapite), 4)
    end as percentile_procapite,
    -- ================================================================
    -- BENCHMARK ALIQUOTA EFFETTIVA
    -- ================================================================
    round(avg(aliquota_effettiva_pct) over (partition by anno), 2) as media_nazionale_aliquota,
    round(avg(aliquota_effettiva_pct) over (partition by anno, regione), 2) as media_regionale_aliquota,
    case
        when aliquota_effettiva_pct is null then null
        else round(percent_rank() over (partition by anno order by aliquota_effettiva_pct), 4)
    end as percentile_aliquota,
    -- ================================================================
    -- RANK (regionale)
    -- ================================================================
    row_number() over (partition by anno, regione order by reddito_medio_per_contribuente desc) as rank_regionale_reddito,
    row_number() over (partition by anno, regione order by aliquota_effettiva_pct desc) as rank_regionale_aliquota,
    -- ================================================================
    -- FASCE QUALITATIVE
    -- ================================================================
    case
        when percent_rank() over (partition by anno order by reddito_medio_per_contribuente) >= 0.8 then 'ELEVATO'
        when percent_rank() over (partition by anno order by reddito_medio_per_contribuente) >= 0.6 then 'SOPRA_MEDIA'
        when percent_rank() over (partition by anno order by reddito_medio_per_contribuente) >= 0.4 then 'MEDIA'
        when percent_rank() over (partition by anno order by reddito_medio_per_contribuente) >= 0.2 then 'SOTTO_MEDIA'
        else 'BASSO'
    end as fascia_reddito
from base
order by anno, regione, denominazione_comune;
