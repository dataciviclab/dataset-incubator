select
  cast_int("Anno")                                           as anno,
  cast_int("Mese")                                           as mese,
  normalize_string("Ministero")                              as ministero,
  normalize_string("Capitolo di Bilancio")                   as capitolo_bilancio,
  normalize_string("Piano di Gestione")                      as piano_gestione,
  normalize_string("Desc. Cap.Bilancio-Piano Gest.")         as descrizione_capitolo,
  normalize_string("RTS")                                    as rts,
  normalize_string("Descrizione RTS")                        as descrizione_rts,
  cast_int("Numero Partite")                                 as numero_partite,
  cast_double("Importi ARRETRATI")                           as importi_arretrati_eur,
  cast_double("Importi RATEI")                               as importi_ratei_eur,
  cast_double("Importi TREDICESIMA")                         as importi_tredicesima_eur,
  cast_double("Importi TOTALE")                              as importi_totale_eur
from raw_input
where cast_int("Anno") is not null
  and cast_int("Numero Partite") is not null
