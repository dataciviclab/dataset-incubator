select
    "Codice Provincia" as provincia_codice,
    "Provincia" as provincia,
    cast("Istituzioni non profit" as integer) as istituzioni,
    cast("Dipendenti" as integer) as dipendenti
from raw_input
where "Codice Provincia" is not null
  and "Provincia" is not null
