-- mart.sql — malasanita_struttura_mortalita — mart_regioni_2022
-- TODO: definire dopo verifica CSV A/B/C/D e stabilizzazione del clean
--
-- Struttura attesa:
--   - join regionale tra personale sanitario (fonti A/B/C) e mortalita evitabile (fonte D)
--   - chiave di join: codice_regione ISTAT (2 cifre)
--   - output: una riga per regione con indicatori chiave 2022
--   - escludere Emilia-Romagna dall'analisi principale (benchmark opzionale)

select
  *
from clean_input
