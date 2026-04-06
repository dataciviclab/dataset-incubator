select
    anno,
    regione,
    pres_aff_imp,
    gini
from clean_input
order by anno, regione, pres_aff_imp
