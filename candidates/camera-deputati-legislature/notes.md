# Notes — camera-deputati-legislature

## 2026-04-26 — Runnable

- Pipeline completata: raw ✅ clean ✅ mart ✅
- Struttura flatten da nested a single-source
- Query SPARQL fixata: `dct:title` non esiste → `REPLACE` su URI
- Raw rifatto con 10k righe (LIMIT 50000)
- Tutti i layer validano OK

## Source

- Endpoint: `https://dati.camera.it/sparql` — RD93 / OpenData Camera
- Probe: ~55k deputati totali, 10k nel campione (LIMIT 50000)
- Nota: endpoint può dare 503 intermittenti — raw scaricato via fetch diretto

## Blocker risolti

1. **Bug `_format_args` toolkit**: `.format(year=year)` su ogni stringa → `KeyError` su SPARQL con `{`. Fix: `"{year}" in v` prima di formattare.
2. **Query SPARQL**: `?leg dct:title ?legislatura` restituiva sempre null. Fix: estrazione da URI con `REPLACE(STR(?leg), ..., '')`.
3. **Typo colonna**: `legislature` vs `legislatura` in mart.sql.

## Dato

- Ogni deputato può apparire in più legislature → la chiave è `(deputato, legislature)`
- Nessuna aggregazione numerica — è un dataset a livello persona
- `legislatura` è un intero roman/arabico in stringa ("17", "18"...)

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
