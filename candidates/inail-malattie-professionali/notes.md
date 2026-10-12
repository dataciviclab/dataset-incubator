# Notes — inail-malattie-professionali

## Quirk della fonte

- **CSV diretto, non CKAN**: il download funziona via `GET https://dati.inail.it/opendata/downloads/...`. Niente API CKAN necessaria.
- **Delimiter `;`**: tutti i CSV INAIL usano punto e virgola.
- **Date formato gg/mm/aaaa**: il clean usa `TRY_CAST(... AS DATE)` — DuckDB parsa correttamente il formato europeo.
- **REST API rotta**: `dati.inail.it/api/OpenData/...` restituisce HTTP 500 con qualsiasi combinazione di parametri. Solo `DataDec` funziona. Usare i CSV diretti.
- **Infortuni bloccati**: i dataset infortuni restituiscono `Content-Length: 0` (file vuoto) e API 500. Probabilmente rimossi o in manutenzione. Da riprovare in futuro.
- **102 item → 5 famiglie**: l'inventario CKAN ha 102 item ma sono 5 famiglie logiche × 19-21 regioni. Il file Italia è sufficiente.
- **ID lavoratore/caso esclusi dal clean**: microdati con identificativi — non committare, non esporre. Il clean li droppa per privacy.

## Decisioni metodologiche

- **Solo il file Italia**: i CSV per-regione hanno lo stesso schema. Il file Italia è il censimento completo.
- **Snapshot, non serie storica**: il semestrale è uno snapshot al momento della pubblicazione. Ogni run sovrascrive. La serie storica si costruisce con i run multi-anno (toolkit gestisce).
- **4 mart**: settore, agente causale, menomazione, genere — le 4 dimensioni analitiche principali.
- **primary_key nei mart**: derivata dal GROUP BY di ciascuna query.

## Rischi noti

- **Privacy**: i dati contengono ID lavoratore e caso. Il clean li esclude, ma il raw li contiene. Non committare raw.
- **Fonte instabile**: INAIL ha periodi di manutenzione (il sito è stato down durante lo scouting). Il timeout del raw è 300s.
- **Snapshot unico**: senza storico, un'analisi temporale richiede più run nel tempo.
- **Codici regione INAIL**: numerici (es. "19" = Lombardia), non ISO. Il clean usa `SedeInailCompetente` come stringa libera.
