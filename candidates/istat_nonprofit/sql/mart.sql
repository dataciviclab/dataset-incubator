select
    provincia_codice,
    provincia,
    istituzioni,
    dipendenti,
    istituzioni + dipendenti as totale_risorse_coinvolte
from clean_input
order by provincia_codice
