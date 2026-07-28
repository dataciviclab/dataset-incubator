-- mart_sintesi — IRPEF Comunale: statistiche regionali + fonti + diseguaglianza
--
-- Unisce i vecchi: irpef_by_regione + mart_fonti_reddito + mart_diseguaglianza.
-- Output: 1 riga = 1 regione × anno (~120 righe).
--
-- Include:
--   • Statistiche aggregate: contribuenti, redditi, imposte, aliquota media
--   • Composizione fonti di reddito (quote %)
--   • Disuguaglianza intra-regionale (CV, delta max-min)

with
base as (
    select
        anno_di_imposta as anno,
        regione,
        codice_istat_regione,
        numero_contribuenti,
        reddito_imponibile_eur,
        imposta_netta_eur,
        addizionale_comunale_dovuta_eur,
        addizionale_regionale_dovuta_eur,
        reddito_da_lavoro_dipendente_e_assimilati_eur,
        reddito_da_pensione_eur,
        reddito_da_fabbricati_eur,
        reddito_da_partecipazione_eur,
        reddito_da_lavoro_autonomo_comprensivo_valori_nulli_eur,
        reddito_complessivo_eur,
        -- Reddito medio per contribuente (per diseguaglianza)
        reddito_imponibile_eur / nullif(numero_contribuenti, 0) as reddito_medio
    from clean_input
    where regione is not null
      and numero_contribuenti > 0
      and reddito_imponibile_eur > 0
),
aggregati_regione as (
    select
        anno,
        regione,
        max(codice_istat_regione) as codice_istat_regione,
        count(*) as comuni,
        sum(numero_contribuenti) as contribuenti_totale,
        sum(reddito_imponibile_eur) as reddito_imponibile_totale_eur,
        sum(imposta_netta_eur) as imposta_netta_totale_eur,
        sum(addizionale_comunale_dovuta_eur) as addizionale_comunale_totale_eur,
        sum(addizionale_regionale_dovuta_eur) as addizionale_regionale_totale_eur,
        -- Aliquota effettiva media regionale (pesata su reddito)
        sum(imposta_netta_eur) * 100.0 / nullif(sum(reddito_imponibile_eur), 0) as aliquota_effettiva_media_pct,
        -- Reddito medio regionale (pesato su contribuenti)
        sum(reddito_imponibile_eur) / nullif(sum(numero_contribuenti), 0) as reddito_medio_regionale,
        -- Fonti di reddito (quote % sul reddito complessivo)
        case when sum(reddito_complessivo_eur) > 0 then
            round(sum(reddito_da_lavoro_dipendente_e_assimilati_eur) * 100.0 / sum(reddito_complessivo_eur), 2)
        end as quota_lavoro_dip_pct,
        case when sum(reddito_complessivo_eur) > 0 then
            round(sum(reddito_da_pensione_eur) * 100.0 / sum(reddito_complessivo_eur), 2)
        end as quota_pensione_pct,
        case when sum(reddito_complessivo_eur) > 0 then
            round(sum(reddito_da_fabbricati_eur) * 100.0 / sum(reddito_complessivo_eur), 2)
        end as quota_fabbricati_pct,
        case when sum(reddito_complessivo_eur) > 0 then
            round(sum(reddito_da_partecipazione_eur) * 100.0 / sum(reddito_complessivo_eur), 2)
        end as quota_partecipazione_pct,
        case when sum(reddito_complessivo_eur) > 0 then
            round(sum(reddito_da_lavoro_autonomo_comprensivo_valori_nulli_eur) * 100.0 / sum(reddito_complessivo_eur), 2)
        end as quota_autonomo_pct,
        -- Disuguaglianza intra-regionale
        round(min(reddito_medio), 0) as reddito_medio_min,
        round(max(reddito_medio), 0) as reddito_medio_max,
        round(avg(reddito_medio), 0) as reddito_medio_medio,
        round(max(reddito_medio) - min(reddito_medio), 0) as delta_max_min_reddito,
        round(stddev_samp(reddito_medio), 0) as devstd_reddito,
        round(stddev_samp(reddito_medio) * 100.0 / nullif(avg(reddito_medio), 0), 2) as cv_reddito_pct,
        round(max(reddito_medio) * 1.0 / nullif(min(reddito_medio), 1), 1) as rapporto_max_min_reddito
    from base
    group by anno, regione
)
select
    anno,
    regione,
    codice_istat_regione,
    comuni,
    contribuenti_totale,
    reddito_imponibile_totale_eur,
    imposta_netta_totale_eur,
    addizionale_comunale_totale_eur,
    addizionale_regionale_totale_eur,
    round(aliquota_effettiva_media_pct, 2) as aliquota_effettiva_media_pct,
    round(reddito_medio_regionale, 0) as reddito_medio_regionale,
    -- Fonti di reddito
    quota_lavoro_dip_pct,
    quota_pensione_pct,
    quota_fabbricati_pct,
    quota_partecipazione_pct,
    quota_autonomo_pct,
    -- Indicatore dipendenza da pensione
    quota_pensione_pct as dipendenza_pensione_pct,
    -- Disuguaglianza
    reddito_medio_min,
    reddito_medio_max,
    reddito_medio_medio,
    delta_max_min_reddito,
    devstd_reddito,
    cv_reddito_pct,
    rapporto_max_min_reddito
from aggregati_regione
order by anno desc, reddito_imponibile_totale_eur desc;
