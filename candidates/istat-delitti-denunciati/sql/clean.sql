with normalized as (
    select
        try_cast(period as integer) as anno,
        series_name,
        regexp_extract(series_name, 'A\.IT\.CRIMEN\.([^.]+)\.9\.YRDUR', 1) as codice_reato,
        try_cast(numero_denunce as double) as numero_denunce
    from raw_input
    unpivot (
        numero_denunce for series_name in (columns(* exclude (period)))
    )
)
select
    anno,
    'IT' as codice_territorio,
    'Italia' as territorio,
    codice_reato,
    codice_reato as reato,
    numero_denunce
from normalized
where anno between 2010 and 2015
  and codice_reato != ''
  and numero_denunce is not null
