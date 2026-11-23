-- clean.sql: matrice pendolarismo 2021 (lavoro + studio)
-- Due file, stesso tracciato con suffisso diverso (_lav / _stu). Con
-- clean.read.mode=all + union_by_name il view raw_input contiene entrambe le
-- coppie di colonne, una nulla per file: il discriminante e' quale Procom_* e'
-- valorizzato. I codici hanno zeri iniziali (001001): all_varchar + cast espliciti.

with base as (
    select
        case when Procom_lav is not null then 'lavoro' else 'studio' end as motivo,
        normalize_string(Procom_res) as comune_residenza,
        coalesce(
            normalize_string(Procom_lav),
            normalize_string(Procom_stu)
        ) as comune_destinazione,
        cast_int(Pendolari) as pendolari
    from raw_input
)

select
    motivo,
    comune_residenza,
    comune_destinazione,
    pendolari
from base
where comune_residenza is not null
  and comune_destinazione is not null
  and pendolari is not null
  and pendolari > 0
order by motivo, pendolari desc
