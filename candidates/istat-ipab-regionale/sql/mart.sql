select
    trimestre,
    area_codice,
    area,
    livello_geografico,
    tipo_abitazione,
    tipo_abitazione_label,
    indice_prezzi
from clean_input
where trimestre is not null
order by trimestre, livello_geografico, area_codice, tipo_abitazione
