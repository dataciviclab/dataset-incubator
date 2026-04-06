select
    anno,
    regione_codice,
    regione,
    pres_aff_imp,
    gini
from clean_input
order by anno, regione_codice, pres_aff_imp
