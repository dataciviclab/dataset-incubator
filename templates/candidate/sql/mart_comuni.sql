-- mart_comuni — arricchimento territoriale + benchmark tra comuni
--
-- ATTIVARE SOLO se il dataset ha granularità comunale O provinciale
-- con almeno una metrica quantitativa confrontabile (kg, €, %, ore, ecc.).
--
-- Output: STESSA cardinalità del clean (1 riga = 1 osservazione).
-- Ogni riga viene arricchita con:
--   • coordinate territoriali (regione, provincia, macro-area, classe demografica)
--   • valori pro-capite (se popolazione disponibile)
--   • benchmark nazionale e di confronto tra simili
--
-- Personalizzazione:
--   1. Sostituisci {codice_istat} con la colonna codice ISTAT 6 cifre
--   2. Sostituisci {metrica_1}, {metrica_2} con le colonne da benchmarkare
--   3. Se il dataset non ha codice_istat ma ha provincia/regione,
--      attiva la SEZIONE B invece di comuni_master
--   4. Se la popolazione non serve, commenta la join popolazione
--   5. Regola le soglie della fascia qualitativa se serve

with
-- Dati territoriali di riferimento
comuni_master as (
    select
        codice_istat,
        denominazione,
        regione,
        provincia as provincia_nome,
        substr(codice_istat, 1, 3) as prov_cod,
        flag_capoluogo,
        -- classe demografica (popolazione 2024 o anno più recente)
        case
            when popolazione_residente < 5000       then 'A_MENO_5K'
            when popolazione_residente < 15000      then 'B_5K_15K'
            when popolazione_residente < 50000      then 'C_15K_50K'
            when popolazione_residente < 250000     then 'D_50K_250K'
            else                                          'E_OLTRE_250K'
        end as classe_demografica,
        -- macro-area geografica
        case
            when regione in ('Valle d''Aosta', 'Piemonte', 'Liguria', 'Lombardia',
                             'Trentino-Alto Adige', 'Veneto', 'Friuli-Venezia Giulia',
                             'Emilia-Romagna') then 'NORD'
            when regione in ('Toscana', 'Umbria', 'Marche', 'Lazio') then 'CENTRO'
            else 'SUD_ISOLE'
        end as macro_area
    from read_parquet('{support.comuni_master.mart}')
),
-- -- SEZIONE B (alternativa): se non hai codice_istat ma hai provincia/regione
-- -- Scommenta e adatta se il dataset arriva già con provincia e regione
-- -- ma senza codice ISTAT comunale.
-- territori as (
--     select distinct
--         regione,
--         provincia,
--         -- popolazione aggregata per provincia se serve
--     from clean_input
-- )

base as (
    select
        -- Colonne originali del clean (esplicite per chiarezza)
        t.*,
        -- Arricchimento territoriale
        cm.regione               as regione,
        cm.provincia_nome        as provincia,
        cm.macro_area,
        cm.classe_demografica,
        cm.flag_capoluogo,
        cm.denominazione         as denominazione_comune
    from clean_input t
    left join comuni_master cm
        on t.{codice_istat} = cm.codice_istat
),
con_popolazione as (
    select
        b.*,
        p.popolazione_residente
    from base b
    left join read_parquet('{support.popolazione.mart}') p
        on b.{codice_istat} = p.codice_comune
        and b.anno = p.anno
),
benchmark as (
    select
        *,
        -- Valori pro-capite (solo se popolazione disponibile)
        case
            when popolazione_residente > 0
            then {metrica_1} / popolazione_residente
        end as {metrica_1}_procapite,
        -- ============================================================
        -- BENCHMARK NAZIONALE (window function, una scansione sola)
        -- ============================================================
        -- Media nazionale dell'indicatore principale
        avg({metrica_1}) over (partition by anno) as media_nazionale,
        -- Media regionale
        avg({metrica_1}) over (partition by anno, regione) as media_regionale,
        -- Media tra comuni della stessa classe demografica
        avg({metrica_1}) over (partition by anno, classe_demografica) as media_classe,
        -- Deviazione standard nazionale (per valutare dispersione)
        stddev({metrica_1}) over (partition by anno) as std_nazionale,
        -- Percentile nazionale (0 = valore più basso, 1 = più alto)
        percent_rank() over (
            partition by anno
            order by {metrica_1}
        ) as percentile_nazionale,
        -- Distanza % dalla media nazionale
        case
            when avg({metrica_1}) over (partition by anno) <> 0
            then ({metrica_1} - avg({metrica_1}) over (partition by anno))
                 / abs(avg({metrica_1}) over (partition by anno)) * 100
        end as distanza_media_nazionale_pct,
        -- Distanza % dalla media di classe
        case
            when avg({metrica_1}) over (partition by anno, classe_demografica) <> 0
            then ({metrica_1} - avg({metrica_1}) over (partition by anno, classe_demografica))
                 / abs(avg({metrica_1}) over (partition by anno, classe_demografica)) * 100
        end as distanza_media_classe_pct,
        -- ============================================================
        -- IDEM per metrica_2 (copia e adatta se serve)
        -- ============================================================
        -- avg({metrica_2}) over (partition by anno) as media_nazionale_2,
        -- percent_rank() over (partition by anno order by {metrica_2}) as percentile_nazionale_2,
    from con_popolazione
    where {codice_istat} is not null
)
select
    *,
    -- Fascia qualitativa (basata sul percentile nazionale)
    case
        when percentile_nazionale is null then null
        when percentile_nazionale >= 0.8 then 'ELEVATO'
        when percentile_nazionale >= 0.6 then 'SOPRA_MEDIA'
        when percentile_nazionale >= 0.4 then 'MEDIA'
        when percentile_nazionale >= 0.2 then 'SOTTO_MEDIA'
        else 'BASSO'
    end as fascia_valore,
    -- Segnali di attenzione
    case
        when distanza_media_nazionale_pct is null then null
        when abs(distanza_media_nazionale_pct) > 50 then 'OUTLIER'
        when abs(distanza_media_nazionale_pct) > 25 then 'DISCORDE'
        else 'COERENTE'
    end as segnale_scostamento
from benchmark
order by anno, {codice_istat};
