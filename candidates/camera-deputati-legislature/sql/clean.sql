-- Clean: camera_deputati_legislature
-- I deputati storici (Regno) hanno nome/cogn in rdfs:label
-- formato: "NOME COGNOME, Legislatura XX del Regno"
-- I deputati recenti (Repubblica) hanno foaf:surname + foaf:firstName
-- Qui unifichiamo: estraiamo da label se mancanti, altrimenti usiamo i campi diretti
--
-- Estensione 2026-08-03 (issue #787):
--   - persona_id: id numerico della persona dall'URI (ponte verso senato/governo)
--   - biografia, foto_url, mandato, scheda_url: anagrafica dalla fonte

SELECT
  deputato,
  -- id numerico della persona dall'URI deputato.rdf/d302103_17 → 302103
  TRY_CAST(
    CASE
      WHEN deputato LIKE '%/deputato.rdf/d%' AND deputato NOT LIKE '%/deputato.rdf/dr%' THEN
        regexp_extract(deputato, 'deputato\.rdf/d(\d+)_', 1)
      WHEN deputato LIKE '%/deputato.rdf/dr%' THEN
        regexp_extract(deputato, 'deputato\.rdf/dr(\d+)_', 1)
    END AS BIGINT
  ) AS persona_id,
  CASE
    WHEN cogn IS NOT NULL AND cogn != '' THEN normalize_string(cogn)
    -- label: "NOME COGNOME, Legislatura..." → ultima parola prima della virgola = cognome
    WHEN label IS NOT NULL THEN
      TRIM(REVERSE(SPLIT_PART(REVERSE(SPLIT_PART(label, ',', 1)), ' ', 1)))
    ELSE NULL
  END AS cognome,
  CASE
    WHEN nome IS NOT NULL AND nome != '' THEN normalize_string(nome)
    -- label: "NOME COGNOME, Legislatura..." → tutto tranne l'ultima parola = nome
    WHEN label IS NOT NULL THEN
      TRIM(SUBSTRING(SPLIT_PART(label, ',', 1), 1,
        LENGTH(SPLIT_PART(label, ',', 1)) - LENGTH(REVERSE(SPLIT_PART(REVERSE(SPLIT_PART(label, ',', 1)), ' ', 1))) - 1))
    ELSE NULL
  END AS nome,
  normalize_string(gender) AS gender,
  normalize_string(legislatura) AS legislatura,
  normalize_string(biografia) AS biografia,
  normalize_string(foto) AS foto_url,
  normalize_string(mandato) AS mandato,
  normalize_string(scheda) AS scheda_url
FROM raw_input
