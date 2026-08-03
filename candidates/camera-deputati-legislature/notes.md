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

## 2026-08-03 — estensione issue #787 (approccio A: semplice)

### Cosa è cambiato
- years: 2024 → 2026 (anno di run corrente)
- Query SPARQL: GROUP BY ?deputato + MAX() (fix duplicati da OPTIONAL multipli) —
  recupera il gap: 27.764 deputati (prima 27.618)
- accept_format: "sparql-results+json" (con "csv" l'endpoint restituisce Turtle!)
- Colonne nuove: persona_id, biografia, foto_url, mandato, scheda_url
- Mart serie (no pass-through): mart_legislatura_genere, mart_top_mandati
  (aggregata per persona_id — un deputato URI è per-legislatura)

### persona_id — chiave standard
- Estratto dall'URI deputato.rdf/d302103_17 → 302103 (regexp)
- Deputati del Regno hanno URI dr56_26 (con 'r') → secondo pattern
- 11.276 persone distinte su 27.764 mandati
- Ponte verso senato/governo (stessa normalizzazione ovunque)

### Legislatura — formato uniforme
- Ora "repubblica_17" / "regno_21" / "costituente" (nome completo, niente
  REPLACE che toglieva il prefisso) — identico a camera-incarichi
- Join deputati ↔ incarichi su (persona_id, legislatura): 3.096/3.096 (100%)

### Perché NON per-legislatura (approccio B scartato)
- 20 legislature come years × query IF × zero-padding = complessità esplosa
- L'approccio A (query unica pages:3) funziona: 27.764 righe, niente perdita
