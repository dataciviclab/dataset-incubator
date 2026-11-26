select
  cast_int("Anno")                                         as anno,
  cast_int("Mese")                                         as mese,
  normalize_string("Distribuzione territoriale")           as regione,
  normalize_string("Sigla")                                as sigla_provincia,
  normalize_string("Ufficio")                              as ufficio,
  normalize_string("Tipo Pensione")                        as tipo_pensione,
  normalize_string("Codice Tipo Pensione")                 as codice_tipo_pensione,
  normalize_string("Descrizione pensione")                 as descrizione_pensione,
  normalize_string("Codice pensione")                      as codice_pensione,
  normalize_string("Descrizione microqualifica")           as descrizione_microqualifica,
  normalize_string("Codice microqualifica")                as codice_microqualifica,
  normalize_string("Codice Titolo")                        as codice_titolo,
  normalize_string("Titolo")                               as titolo,
  cast_int("Numero Partite")                               as numero_partite,
  cast_double("Importi ARRETRATI")                         as importi_arretrati_eur,
  cast_double("Importi RATEI")                             as importi_ratei_eur,
  cast_double("Importi TREDICESIMA")                       as importi_tredicesima_eur,
  cast_double("Importi mensili pagati")                    as importi_mensili_pagati_eur
from raw_input
where cast_int("Anno") is not null
  and cast_int("Numero Partite") is not null
