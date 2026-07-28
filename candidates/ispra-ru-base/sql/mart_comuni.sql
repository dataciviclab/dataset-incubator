-- mart_comuni — ISPRA Rifiuti Urbani: arricchimento + benchmark comunale
--
-- Unisce i vecchi: mart.sql (kg_procapite) + mart_ranking_comuni (classi + rank)
-- + parti di mart_rd_provincia e mart_kg_procapite (benchmark nazionale/regionale).
--
-- Stessa cardinalità del clean (1 riga = 1 comune × anno).
-- Ogni riga arricchita con:
--   • kg pro-capite calcolati
--   • classe demografica (per confronto tra simili)
--   • benchmark: media nazionale/regionale, percentile, fascia, distanza %
--
-- Uso: analisi territoriali, unified_comuni, ranking civico.
-- Le aggregazioni semplici (GROUP BY provincia) si fanno ad-hoc con clean-query.

with
comuni_con_classi as (
    select
        anno,
        codice_comune_istat,
        regione,
        provincia,
        comune,
        popolazione,
        totale_ru_tonnellate,
        totale_rd_tonnellate,
        percentuale_rd,
        -- kg pro-capite (era in mart.sql)
        round(totale_ru_tonnellate * 1000.0 / nullif(popolazione, 0), 3) as kg_ru_per_abitante,
        round(totale_rd_tonnellate * 1000.0 / nullif(popolazione, 0), 3) as kg_rd_per_abitante,
        -- classe demografica ISPRA (era in mart_ranking_comuni)
        case
            when popolazione < 5000  then 'A_MENO_5K'
            when popolazione < 15000 then 'B_5K_15K'
            when popolazione < 50000 then 'C_15K_50K'
            else                          'D_OLTRE_50K'
        end as classe_demografica
    from clean_input
    where popolazione > 0
)
select
    *,
    -- ================================================================
    -- BENCHMARK — window functions (una scansione sola)
    -- ================================================================
    -- Media nazionale RD%
    round(avg(percentuale_rd) over (partition by anno), 2)                                         as media_nazionale_rd,
    -- Media regionale RD%
    round(avg(percentuale_rd) over (partition by anno, regione), 2)                                as media_regionale_rd,
    -- Media tra comuni della stessa classe demografica
    round(avg(percentuale_rd) over (partition by anno, classe_demografica), 2)                     as media_classe_rd,
    -- Deviazione standard nazionale RD%
    round(stddev(percentuale_rd) over (partition by anno), 2)                                       as std_nazionale_rd,
    -- Percentile nazionale RD% (0 = peggiore, 1 = migliore; NULL se RD% non disponibile)
    case
        when percentuale_rd is null then null
        else round(percent_rank() over (partition by anno order by percentuale_rd), 4)
    end                                                                                            as percentile_nazionale,
    -- Distanza % dalla media nazionale
    case
        when avg(percentuale_rd) over (partition by anno) <> 0
        then round((percentuale_rd - avg(percentuale_rd) over (partition by anno))
             / abs(avg(percentuale_rd) over (partition by anno)) * 100, 2)
    end                                                                                            as distanza_media_nazionale_pct,
    -- Distanza % dalla media regionale
    case
        when avg(percentuale_rd) over (partition by anno, regione) <> 0
        then round((percentuale_rd - avg(percentuale_rd) over (partition by anno, regione))
             / abs(avg(percentuale_rd) over (partition by anno, regione)) * 100, 2)
    end                                                                                            as distanza_media_regionale_pct,
    -- IDEM per kg_ru_per_abitante
    round(avg(kg_ru_per_abitante) over (partition by anno), 1)                                     as media_nazionale_kg_ru,
    round(avg(kg_ru_per_abitante) over (partition by anno, regione), 1)                            as media_regionale_kg_ru,
    round(percent_rank() over (partition by anno order by kg_ru_per_abitante), 4)                  as percentile_kg_ru,
    -- Rank per classe demografica (era in mart_ranking_comuni)
    case
        when percentuale_rd is null then null
        else row_number() over (partition by anno, classe_demografica order by percentuale_rd desc)
    end                                                                                            as rank_classe_rd,
    -- Fascia qualitativa (solo se percentuale_rd non è NULL)
    case
        when percentuale_rd is null then null
        when percent_rank() over (partition by anno order by percentuale_rd) >= 0.8 then 'ELEVATO'
        when percent_rank() over (partition by anno order by percentuale_rd) >= 0.6 then 'SOPRA_MEDIA'
        when percent_rank() over (partition by anno order by percentuale_rd) >= 0.4 then 'MEDIA'
        when percent_rank() over (partition by anno order by percentuale_rd) >= 0.2 then 'SOTTO_MEDIA'
        else 'BASSO'
    end                                                                                            as fascia_rd
from comuni_con_classi
order by anno, regione, provincia, comune;
