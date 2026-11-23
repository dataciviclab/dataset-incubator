-- mart_flussi_top: le 200 coppie origine-destinazione piu' consistenti
-- (solo flussi tra comuni diversi), con i nomi dei due comuni.
with f as (
    select motivo, comune_residenza, comune_destinazione, pendolari
    from clean_input
    where comune_residenza <> comune_destinazione
    order by pendolari desc
    limit 200
),
comuni as (
    select codice_istat, denominazione, provincia, regione
    from read_parquet({support.comuni.clean})
)
select
    f.motivo,
    f.comune_residenza,
    cr.denominazione as comune_residenza_nome,
    cr.provincia as provincia_residenza,
    f.comune_destinazione,
    cd.denominazione as comune_destinazione_nome,
    cd.provincia as provincia_destinazione,
    f.pendolari
from f
left join comuni cr on cr.codice_istat = f.comune_residenza
left join comuni cd on cd.codice_istat = f.comune_destinazione
order by f.pendolari desc
