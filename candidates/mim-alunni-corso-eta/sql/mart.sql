-- Mart: alunni per corso/eta — dati arricchiti per livello scuola
SELECT
  anno_scolastico,
  codice_scuola,
  denominazione_scuola,
  ordine_scuola,
  grado_istruzione_scuola,
  anno_corso,
  fascia_eta,
  alunni,
  area_geografica,
  regione,
  provincia,
  comune,
  codice_comune_scuola,
  denominazione_istituto_riferimento
FROM clean_input
