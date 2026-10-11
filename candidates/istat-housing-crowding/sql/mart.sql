-- mart: serie annuale Italia per titolo di godimento (righe di totale su
-- tutte le breakdown dimension — l'indagine originale, senza varianti)
select
    anno,
    ref_area_codice,
    ref_area,
    titolo_godimento_codice,
    titolo_godimento,
    componenti_per_100mq
from clean_input
where ref_area_codice = 'IT'
  and titolo_godimento_codice in ('1', '2')
  and numero_componenti_nucleo = 99
  and tipologia_nucleo_codice = '99'
  and numero_figli = 9
  and numero_anziani = 9
  and quintile_reddito_codice = '9'
  and sesso_percettore_principale_codice = '9'
  and eta_percettore_principale_codice = '9'
  and titolo_studio_percettore_codice = '99'
  and condizione_professionale_percettore_codice = '99'
order by anno, titolo_godimento_codice
