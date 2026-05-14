with base as (
    select
        try_cast(Anno_decorrenza as integer) as anno,
        case Trimestrale
            when 'I trimestre' then 1
            when 'II trimestre' then 2
            when 'III trimestre' then 3
            when 'IV trimestre' then 4
            else null
        end as trimestre,
        trim(SESSO) as sesso,
        trim(classe_eta) as classe_eta,
        trim(classe_importo) as classe_importo,
        trim(area_geografica) as area_geografica,
        trim(gestione) as gestione,
        trim(tgestio) as tipo_gestione,
        trim(Categoria) as categoria,
        trim(Regione) as regione,
        try_cast(Numero_pensioni as double) as numero_pensioni
    from raw_input
)
select
    anno,
    trimestre,
    sesso,
    classe_eta,
    classe_importo,
    area_geografica,
    gestione,
    tipo_gestione,
    categoria,
    regione,
    numero_pensioni
from base
where anno between 2020 and 2024
  and trimestre between 1 and 4
  and regione is not null
  and regione <> ''
  and numero_pensioni is not null;
