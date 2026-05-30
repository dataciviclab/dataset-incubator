# Notes — camera-deputati-legislature

## 2026-05-30 — 100% copertura con paginazione

- Pipeline completata: raw ✅ clean ✅ mart ✅
- **27.764 deputati** (100%, endpoint) — prima 10.000 (36%)
- Fix: paginazione SPARQL con `pages: 3, step: 10000`
- Aggiunto supporto `pages`/`step` al plugin SPARPL del toolkit

## 2026-04-26 — Runnable (prima versione, 10k righe)

- Pipeline completata
- Query SPARQL fixata: `dct:title` non esiste → `REPLACE` su URI
- Raw con 10k righe (troncato WAF)

## Source

- Endpoint: `https://dati.camera.it/sparql` — Virtuoso / OpenData Camera
- 27.764 deputati totali (tutte le legislature, dalla Costituente alla XIX)
- Nota: endpoint può dare 503 intermittenti

## Blocker risolti

1. **Paginazione WAF**: plugin SPARQL esteso con `pages`/`step` — esegue query multiple con OFFSET incrementale e concatena CSV
2. **Bug `_format_args` toolkit**: `.format(year=year)` su ogni stringa → `KeyError` su SPARQL con `{` — fixato
3. **Query SPARQL**: `?leg dct:title ?legislatura` restituiva sempre null — fix: `REPLACE` su URI

## Dato

- Ogni deputato può apparire in più legislature → la chiave è `(deputato, legislature)`
- 27.764 righe, nessuna aggregazione
- `legislatura` in formato stringa ("costituente", "regno_01", ..., "repubblica_19")

## Struttura

```
camera-deputati-legislature/
├── dataset.yml          # entrypoint
├── README.md
├── notes.md
├── sql/
│   ├── clean.sql       # raw-faithful (5 cols)
│   └── mart.sql        # deduplicazione + ORDER BY
└── notebooks/
    └── camera_deputati_legislature_v0.ipynb
```
