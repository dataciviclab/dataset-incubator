# Notes — camera-votazioni-sparql

## 2026-05-30 — Pipeline completata

- Pipeline completata: raw ✅ clean ✅ mart ✅
- 8 anni (2018-2025), ~27k votazioni totali
- Query SPARQL con filtro `STRSTARTS(?data, "{year}")` per aggirare WAF
- Fix `_format_args` toolkit: sostituito `str.format()` con `str.replace()` per SPARQL

## Source

- Endpoint: `https://dati.camera.it/sparql` — Virtuoso su Camera dei deputati
- 255k votazioni totali (dal 1996)
- WAF blocca risposte >10k righe
- Content-Type: `text/html` (pagina errore) ma corpo CSV valido

## Blocker risolti

1. **WAF 10k**: risolto con filtro per anno (`FILTER (STRSTARTS(?data, "{year}"))`)
2. **FORMAT crash**: `str.format()` su query SPARQL con `{}` — fix in `_format_args`
3. **Duplicati**: `SELECT DISTINCT` non bastava (OPTIONAL dava righe multiple) — fix: `GROUP BY ?votazione` con `MAX()`

## Dato

- Ogni votazione ha URI univoco (`ocd:votazione.rdf/vs19_XXX`)
- `data` in formato `YYYYMMDD` (BIGINT), pulito con `TRY_STRPTIME(data::VARCHAR, '%Y%m%d')`
- `approvato`, `votazioneFinale`, `votazioneSegreta`, `richiestaFiducia` arrivano come `0`/`1` (BIGINT) → cast a BOOLEAN

## Struttura

```
camera-votazioni-sparql/
├── dataset.yml          # SPARQL query con {year}
├── README.md
├── notes.md
├── sql/
│   ├── clean.sql        # cast tipi + parsing date
│   └── mart.sql         # raw-faithful
```
