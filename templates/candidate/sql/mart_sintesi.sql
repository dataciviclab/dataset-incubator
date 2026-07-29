-- mart_sintesi — statistiche descrittive per livello/gruppo
--
-- SEMPRE ATTIVO. Produce una vista riassuntiva del dataset con
-- statistiche descrittive per gruppo omogeneo (anno, categoria, area, ecc.).
--
-- Duplica righe? SÌ, ogni riga = (gruppo × metrica × statistica).
-- Questo formato "long" è pensato per composizione successiva
-- (unified_comuni, dashboard aggregata) e per export diretto.
--
-- Personalizzazione:
--   1. Sostituisci {chiave_gruppo} con la/e colonna/e di raggruppamento
--      (es. anno, anno+categoria, regione, provincia, ecc.)
--   2. Sostituisci {metrica} con la colonna numerica da descrivere
--      (es. valore, importo, percentuale, ecc.)
--   3. Se hai più metriche, moltiplica la sezione stats.
--   4. Regola la soglia outlier (3 * stddev) se serve.

with
stats as (
    select
        {chiave_gruppo},
        count(*)                                        as n_osservazioni,
        count({metrica})                                as n_non_nulli,
        avg({metrica})                                  as media,
        median({metrica})                               as mediana,
        stddev({metrica})                               as std_dev,
        min({metrica})                                  as minimo,
        max({metrica})                                  as massimo,
        -- primo e terzo quartile via percentile_cont
        percentile_cont(0.25) within group (order by {metrica}) as q1,
        percentile_cont(0.75) within group (order by {metrica}) as q3,
        -- somma (utile per metriche additive: importi, kg, ecc.)
        sum({metrica})                                  as totale
    from clean_input
    group by {chiave_gruppo}
),
outlier_flag as (
    select
        s.*,
        -- Identifica outlier a livello di gruppo
        (s.q3 - s.q1) * 1.5 as iqr,
        s.media - 3 * s.std_dev as soglia_inferiore,
        s.media + 3 * s.std_dev as soglia_superiore
    from stats s
)
select
    *,
    case
        when n_non_nulli < n_osservazioni * 0.5 then 'ALTA_MISSING'
        when n_osservazioni < 3 then 'CAMPIONE_TROPPO_PICCOLO'
        when std_dev = 0 then 'VARIANZA_ZERO'
        else 'OK'
    end as qualita_statistica
from outlier_flag
order by {chiave_gruppo};
