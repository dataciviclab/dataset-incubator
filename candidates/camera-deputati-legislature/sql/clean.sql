-- Clean: camera_deputati_legislature
-- I deputati storici (Regno) hanno nome/cogn in rdfs:label
-- formato: "NOME COGNOME, Legislatura XX del Regno"
-- I deputati recenti (Repubblica) hanno foaf:surname + foaf:firstName
-- Qui unifichiamo: estraiamo da label se mancanti, altrimenti usiamo i campi diretti

SELECT
  deputato,
  CASE
    WHEN cogn IS NOT NULL AND cogn != '' THEN cogn
    -- label: "NOME COGNOME, Legislatura..." → ultima parola prima della virgola = cognome
    WHEN label IS NOT NULL THEN
      TRIM(REVERSE(SPLIT_PART(REVERSE(SPLIT_PART(label, ',', 1)), ' ', 1)))
    ELSE NULL
  END AS cognome,
  CASE
    WHEN nome IS NOT NULL AND nome != '' THEN nome
    -- label: "NOME COGNOME, Legislatura..." → tutto tranne l'ultima parola = nome
    WHEN label IS NOT NULL THEN
      TRIM(SUBSTRING(SPLIT_PART(label, ',', 1), 1,
        LENGTH(SPLIT_PART(label, ',', 1)) - LENGTH(REVERSE(SPLIT_PART(REVERSE(SPLIT_PART(label, ',', 1)), ' ', 1))) - 1))
    ELSE NULL
  END AS nome,
  legislatura,
  gender
FROM raw_input
