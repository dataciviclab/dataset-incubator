-- mart_anziani_livello — ospiti 65+ per area x livello di assistenza sanitaria.
-- A differenza di 49_37 (dove ELD x livello e' solo nazionale), qui il dettaglio
-- per livello esiste per tutte le 28 aree.
-- is_aggregato = true sulla riga di totale (livello ALL): non sommare.

select
    anno,
    ref_area_codice,
    regione,
    livello_assistenza_codice,
    livello_assistenza,
    ospiti as ospiti_65plus,
    (livello_assistenza_codice = 'ALL') as is_aggregato
from clean_input
where tipo_dato_codice = '89'
  and eta_codice = 'Y_GE65'
  and bisogno_codice = 'ALL'
  and livello_assistenza_codice in ('ALL', 'ABS', 'LOW', 'MED', 'HIGH')
  and (
        ref_area_codice = 'IT'
        or (length(ref_area_codice) = 4 and ref_area_codice <> 'ITDA')
      )
order by anno, ref_area_codice, livello_assistenza_codice
