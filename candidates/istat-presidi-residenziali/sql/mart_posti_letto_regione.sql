-- mart_posti_letto_regione — posti letto operativi per area x tipo di utenza
-- x livello di assistenza sanitaria (assente/basso/medio/alto/totale).
-- E' l'incrocio che isola il perimetro RSA: anziani (ELD) con assistenza
-- sanitaria media/alta. Tutte le altre breakdown sono fissate al totale.

select
    anno,
    ref_area_codice,
    regione,
    tipo_utenza_codice,
    tipo_utenza,
    livello_assistenza_codice,
    livello_assistenza,
    valore as posti_letto
from clean_input
where tipo_dato_codice = '73'
  and tipo_residenzialita_codice = 'ALL'
  and funzione_protezione_sociale_codice = '99'
  and natura_giuridica_codice = '9'
  and tipo_gestore_codice = 'TOT'
  and finanziamento_pubblico_codice = '9'
  and professione_codice = 'ALL'
  and livello_assistenza_codice in ('ALL', 'ABS', 'LOW', 'MED', 'HIGH')
  and (
        ref_area_codice = 'IT'
        or (length(ref_area_codice) = 4 and ref_area_codice <> 'ITDA')
      )
order by anno, ref_area_codice, tipo_utenza_codice, livello_assistenza_codice
