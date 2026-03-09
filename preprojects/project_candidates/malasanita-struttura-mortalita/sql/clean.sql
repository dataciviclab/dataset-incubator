-- clean.sql — malasanita_struttura_mortalita
-- TODO: definire dopo verifica CSV A/B/C/D
--
-- Struttura attesa:
--   - normalizzare codice_regione (2 cifre, chiave di join)
--   - selezionare colonne rilevanti per personale sanitario (fonti A, B, C)
--   - selezionare colonne mortalita evitabile (fonte D)
--   - filtrare su anno = 2022

select
  *
from raw_input
