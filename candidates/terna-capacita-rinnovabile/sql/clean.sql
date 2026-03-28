select
    cast("Anno" as integer) as anno,
    trim(cast("Tipo capacità" as varchar)) as tipo_capacita,
    trim(cast("Regione" as varchar)) as regione,
    trim(cast("Provincia" as varchar)) as provincia,
    trim(cast("Fonti" as varchar)) as fonti,
    cast("Potenza efficiente (MW)" as double) as potenza_mw
from raw_input
where try_cast("Anno" as integer) is not null
  and trim(cast("Regione" as varchar)) <> ''
  and trim(cast("Provincia" as varchar)) <> ''
