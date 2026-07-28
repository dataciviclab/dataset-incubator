-- mart_sintesi — ISPRA Rifiuti Urbani: statistiche provinciali
--
-- Unisce i vecchi: mart_rd_provincia (RD% medio) + mart_kg_procapite (kg pro-capite).
-- Entrambi erano GROUP BY provincia × anno — stessa logica, metriche complementari.
--
-- Output: 1 riga = 1 provincia × anno (~1.500 righe).
-- Uso: unified_comuni, dashboard provinciali, confronti territoriali.

select
    anno,
    regione,
    provincia,
    count(*)                                                              as n_comuni,
    round(sum(popolazione), 0)                                            as popolazione_totale,
    -- RD% medio pesato sulla popolazione
    round(sum(percentuale_rd * popolazione) / nullif(sum(popolazione), 0), 2) as rd_media_ponderata,
    -- RD% semplice (media aritmetica tra comuni)
    round(avg(percentuale_rd), 2)                                         as rd_media_semplice,
    round(stddev_samp(percentuale_rd), 2)                                 as rd_devstd,
    round(min(percentuale_rd), 2)                                         as rd_minimo,
    round(max(percentuale_rd), 2)                                         as rd_massimo,
    -- Kg RU pro-capite (pesato su popolazione)
    round(sum(totale_ru_tonnellate * 1000.0) / nullif(sum(popolazione), 0), 1) as kg_ru_procapite,
    -- Kg RD pro-capite (pesato su popolazione)
    round(sum(totale_rd_tonnellate * 1000.0) / nullif(sum(popolazione), 0), 1) as kg_rd_procapite,
    -- Quota RD % calcolata sul peso (coerente con % in tonnellate)
    round(sum(totale_rd_tonnellate) * 100.0 / nullif(sum(totale_ru_tonnellate), 0), 2) as rd_pct_su_peso
from clean_input
where popolazione > 0
  and provincia is not null
group by anno, regione, provincia
order by anno desc, rd_media_ponderata desc;
