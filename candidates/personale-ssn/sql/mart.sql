with base as (
    select
        anno,
        codice_regione,
        denominazione_regione,
        ruolo_categoria,
        coalesce(tempo_pieno_u, 0) + coalesce(part_time_inf_50_u, 0) + coalesce(part_time_sup_50_u, 0) as uomini_totali,
        coalesce(tempo_pieno_d, 0) + coalesce(part_time_inf_50_d, 0) + coalesce(part_time_sup_50_d, 0) as donne_totali,
        coalesce(tempo_pieno_u, 0) + coalesce(tempo_pieno_d, 0) as tempo_pieno_totale,
        coalesce(part_time_inf_50_u, 0) + coalesce(part_time_inf_50_d, 0)
            + coalesce(part_time_sup_50_u, 0) + coalesce(part_time_sup_50_d, 0) as part_time_totale
    from clean_input
    where prospetto = 'TAB1'
)
select
    anno,
    codice_regione,
    denominazione_regione,
    ruolo_categoria,
    sum(uomini_totali + donne_totali) as personale_totale,
    sum(uomini_totali) as uomini_totali,
    sum(donne_totali) as donne_totali,
    sum(tempo_pieno_totale) as tempo_pieno_totale,
    sum(part_time_totale) as part_time_totale,
    round(100.0 * sum(donne_totali) / nullif(sum(uomini_totali + donne_totali), 0), 1) as quota_donne_pct,
    round(100.0 * sum(part_time_totale) / nullif(sum(tempo_pieno_totale + part_time_totale), 0), 1) as quota_part_time_pct
from base
group by 1, 2, 3, 4
order by anno, codice_regione, ruolo_categoria
