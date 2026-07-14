select
    cast(prospetto as varchar) as prospetto,
    cast(anno as integer) as anno,
    cast(codice_regione as varchar) as codice_regione,
    cast(denominazione_regione as varchar) as denominazione_regione,
    cast(codice_azienda as varchar) as codice_azienda,
    case when ruolo_categoria is null or ruolo_categoria = '' then 'ND' else cast(ruolo_categoria as varchar) end as ruolo_categoria,
    dotazioni_organiche,
    tempo_pieno_u,
    tempo_pieno_d,
    part_time_inf_50_u,
    part_time_inf_50_d,
    part_time_sup_50_u,
    part_time_sup_50_d,
    pers_anno_rif_u,
    pers_anno_rif_d
from raw_input
where anno is not null
    and anno between 2010 and 2021
    and codice_regione is not null
