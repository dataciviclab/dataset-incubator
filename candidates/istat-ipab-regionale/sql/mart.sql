select
    trimestre,
    regione_codice,
    regione,
    tipo_abitazione,
    tipo_abitazione_label,
    indice_prezzi
from clean_input
where trimestre is not null
