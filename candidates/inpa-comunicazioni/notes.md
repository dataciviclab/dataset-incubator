## Tecnico

- Fonte: API pubblica non documentata `portale.inpa.gov.it/concorsi-smart/api/communication/user/public-area/search`
- Endpoint paginato Spring (content/totalPages); ~4.244 elementi, ~43 pagine @100
- **Archivio fresco**: solo 2025-2026 nelle pagine popolate; il fondo (pagina 41+) è
  vuoto nonostante totalElements=4244 — verificare la copertura reale a ogni harvest
- CSV flat UTF-8, delimiter `,`, prodotto da `scripts/harvest_comunicazioni.py`
- **Harvest esplicito**: `python scripts/harvest_comunicazioni.py raw_input.csv` genera
  il CSV in `out/data/raw/inpa_comunicazioni/2026/raw_input.csv`. Il `dataset.yml` usa
  `local_file` che legge quel path (niente riesecuzione a ogni run).

## Cautele

- **API non pubblicata né documentata**: schema e disponibilità non garantiti
- **Categoria "Altro"** è il 52% delle comunicazioni — bassa qualità semantica per
  molte voci; le categorie strutturate (graduatorie, calendari, commissioni) sono il 48%
- **`body` è HTML** → strippato nel harvest (testo pulito)
- **`concorso_id` può puntare a bandi non presenti** nello snapshot `inpa-bandi` OPEN
  (concorsi chiusi o non harvestati) — il join bando→esito è completo solo con CLOSED
- **`dateConfirmReceipt` e `mediaDTOList`** non valorizzati nel public endpoint — esclusi

## Decisioni

- Snapshot completo comunicazioni come primo stadio
- `years: [2026]` = anno di snapshot
- `primary_key: [id]` = id comunicazione dell'API
