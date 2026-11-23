-- mart_comuni_pendolarismo: per comune, flussi in entrata/uscita e auto-contenimento
-- Base = comuni di ORIGINE della matrice (non l'anagrafica): 377 comuni sardi hanno
-- codice 2021 diverso da quello dell'elenco comuni 2026 (riforma provinciale), quindi
-- nome/provincia/regione restano NULL invece di far sparire la riga. Il flag
-- `in_anagrafica_2026` rende il gap filtrabile.
--
-- "Uscenti" = residenti che lavorano/studiano fuori comune; "entranti" = non residenti
-- che vengono nel comune. Auto-contenimento = intra / (intra + uscenti): 100% = nessuno esce.
with origini as (
    select
        comune_residenza as cod,
        motivo,
        sum(case when comune_residenza = comune_destinazione then pendolari else 0 end) as intra,
        sum(case when comune_residenza <> comune_destinazione then pendolari else 0 end) as uscenti
    from clean_input
    group by 1, 2
),
destinazioni as (
    select
        comune_destinazione as cod,
        motivo,
        sum(pendolari) as entranti
    from clean_input
    where comune_residenza <> comune_destinazione
    group by 1, 2
),
base as (
    select
        o.cod as codice_istat,
        c.denominazione as comune,
        c.provincia,
        c.regione,
        c.popolazione_residente,
        (c.codice_istat is not null) as in_anagrafica_2026,
        o.motivo,
        coalesce(o.intra, 0) as intra,
        coalesce(o.uscenti, 0) as uscenti,
        coalesce(d.entranti, 0) as entranti
    from origini o
    left join read_parquet({support.comuni.clean}) c on c.codice_istat = o.cod
    left join destinazioni d on d.cod = o.cod and d.motivo = o.motivo
)

select
    codice_istat,
    any_value(comune) as comune,
    any_value(provincia) as provincia,
    any_value(regione) as regione,
    any_value(popolazione_residente) as popolazione_residente,
    bool_or(in_anagrafica_2026) as in_anagrafica_2026,
    sum(case when motivo = 'lavoro' then intra else 0 end) as lavoro_intra,
    sum(case when motivo = 'lavoro' then uscenti else 0 end) as lavoro_uscenti,
    sum(case when motivo = 'lavoro' then entranti else 0 end) as lavoro_entranti,
    sum(case when motivo = 'lavoro' then entranti - uscenti else 0 end) as lavoro_saldo,
    round(
        100.0 * sum(case when motivo = 'lavoro' then intra else 0 end)
        / nullif(sum(case when motivo = 'lavoro' then intra + uscenti else 0 end), 0),
        1
    ) as lavoro_auto_contenimento_pct,
    sum(case when motivo = 'studio' then uscenti else 0 end) as studio_uscenti,
    sum(case when motivo = 'studio' then entranti else 0 end) as studio_entranti
from base
group by 1
order by lavoro_uscenti desc
