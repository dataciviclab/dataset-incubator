select
  try_cast("Anno" as integer)                                       as anno,
  try_cast("Mese" as integer)                                       as mese,
  trim("Distribuzione territoriale")                                as regione,
  trim("Sigla")                                                     as sigla_provincia,
  trim("Ufficio")                                                   as ufficio,
  trim("Tipo Pensione")                                            as tipo_pensione,
  trim("Codice Tipo Pensione")                                      as codice_tipo_pensione,
  trim("Descrizione pensione")                                      as descrizione_pensione,
  trim("Codice pensione")                                           as codice_pensione,
  trim("Descrizione microqualifica")                                as descrizione_microqualifica,
  trim("Codice microqualifica")                                     as codice_microqualifica,
  trim("Codice Titolo")                                             as codice_titolo,
  trim("Titolo")                                                    as titolo,
  try_cast("Numero Partite" as integer)                             as numero_partite,
  try_cast("Importi ARRETRATI" as double)                            as importi_arretrati_eur,
  try_cast("Importi RATEI" as double)                               as importi_ratei_eur,
  try_cast("Importi TREDICESIMA" as double)                         as importi_tredicesima_eur,
  try_cast("Importi mensili pagati" as double)                       as importi_mensili_pagati_eur
from raw_input
where try_cast("Anno" as integer) is not null
  and try_cast("Numero Partite" as integer) is not null
