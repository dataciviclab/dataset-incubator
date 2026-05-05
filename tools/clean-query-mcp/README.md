# Clean Query MCP

Server MCP sperimentale, read-only, per interrogare i clean parquet pubblici del DataCivicLab tramite DuckDB.

Questo tool vive in `dataset-incubator` perché il contratto dei clean ufficiali nasce qui. Il catalogo letto dal server è:

```text
registry/clean_catalog.json
```

Il file locale `datasets.yml` non è più fonte di verità. Il catalogo MCP deve derivare dal Lab Clean Registry.

## Tool

### Scoperta e catalogo

| Tool | Scopo |
|---|---|
| `list_datasets()` | Lista slug disponibili con nome, descrizione, periodo |
| `search_datasets(query)` | Cerca per nome, descrizione o fonte |
| `describe_dataset(slug)` | Schema completo: colonne, tipi, ruolo, periodo |
| `find_metric_datasets(query, metric_name)` | Cerca dataset che abbiano colonne role=metric |
| `column_search(query)` | Cerca sia in meta dataset che in nome/descrizione colonne |

### Esplorazione senza SQL

| Tool | Scopo |
|---|---|
| `preview(dataset, limit, year)` | Prime N righe — no SQL, veloce per capire la struttura |
| `count(dataset, year)` | Conteggio righe totale, con filtro anno opzionale |
| `distinct_values(dataset, column, limit)` | Valori unici di una colonna — utile per UI filter |

### Analisi pre-costruita

| Tool | Scopo |
|---|---|
| `aggregate(dataset, metric, group_by, filters, year)` | Helper: SQL di aggregazione pre-scritto, passa a `run_query()` |
| `time_series(dataset, metric, group_by, year, limit)` | Serie storica metric×dimension nel tempo |

### Query e debug

| Tool | Scopo |
|---|---|
| `run_query(sql, dataset, max_rows, year)` | Query DuckDB read-only — solo SELECT/WITH, hard cap 500 righe |
| `explain_query(sql, dataset)` | Valida SQL senza eseguirla — stima validità e risolve parquet |
| `cache_stats()` | Stato della cache GCS — utile per debug

## Runtime

Da root del repository `dataset-incubator`:

```bash
python -m pip install -r tools/clean-query-mcp/requirements.txt
```

Config MCP:

```json
{
  "mcpServers": {
    "clean-query": {
      "command": "python",
      "args": [
        "/absolute/path/to/dataset-incubator/tools/clean-query-mcp/server.py"
      ]
    }
  }
}
```

## Catalogo

Default:

```text
../../registry/clean_catalog.json
```

Override:

```bash
CLEAN_QUERY_CATALOG_PATH=/path/to/clean_catalog.json
```

Il catalogo è versionato in DI e può essere pubblicato come artifact GCS per consumer downstream:

```text
gs://dataciviclab-clean/catalog/clean_catalog.json
```

## Guardrail

- Solo `SELECT` / `WITH`
- `max_rows` default 100, hard cap 500
- Timeout query 60 secondi
- Memory limit DuckDB: `2GB`
- Keyword DDL/DML bloccate
- Scope enforcement: solo `FROM clean_input` e CTE locali
- Join cross-dataset bloccati
- Accesso diretto a `read_parquet()` / `read_csv()` bloccato nel SQL utente
- GCS pubblico anonimo di default; usa `CLEAN_QUERY_GCS_AUTH=1` solo se serve autenticazione esplicita

## Output workflow — tool per stage

Pipeline: `source → raw → clean → mart → output`

### Post-clean (verifica qualità)

Dopo `toolkit run --config candidates/{slug}/dataset.yml` e push GCS:

```python
# 1. Verifica struttura e righe
preview(slug, limit=5)          # prime righe — ok se non vuoto
count(slug, year=2024)          # conteggio — confronta con atteso

# 2. Verifica schema
describe_dataset(slug)          # colonne, tipi, role — per conferma contract

# 3. Verifica valori chiave
distinct_values(slug, 'regione')  # valori distinti — outlier visibility
```

### Post-mart (analisi readiness)

Dopo mart SQL e output parquet disponibili:

```python
# 1. Serie storica disponibile?
time_series(dataset, metric='spesa_convenzionata', group_by='regione')

# 2. metriche aggregate
aggregate(dataset, metric='totale_ru_tonnellate', group_by=['regione'], year=2024)

# 3. Query esplorativa
run_query("SELECT regione, SUM(...) FROM clean_input GROUP BY regione", dataset)
```

### Pre-publication (validazione)

Prima di aprire Discussion opromuovere su data-explorer:

```python
# 1. Quali dataset hanno metriche simili?
find_metric_datasets(metric_name='spesa')          # per cross-reference
column_search('regione')                            # per capire coverage

# 2. Valida query complessa prima di esporla
explain_query(sql, dataset)                         # senza eseguirla

# 3. Verifica copertura temporale
time_series(dataset, metric='...', group_by='regione', year=None)
```

## Smoke test

```bash
python tools/clean-query-mcp/scripts/smoke.py
```

Limitato a un dataset:

```bash
python tools/clean-query-mcp/scripts/smoke.py --dataset ispra_ru_base
```

## Limiti noti

- Il tool interroga un dataset alla volta.
- Le analisi cross-dataset richiedono una preparazione a monte o un'estensione esplicita del contratto.
- Il catalogo semantico resta manuale finché non verrà generato direttamente dai `dataset.yml` e dai run record DI.

## Aggiornare il catalogo locale

Dopo push GCS via `push_archive.py`, il catalogo locale `registry/clean_catalog.json` viene aggiornato automaticamente. Per sincronizzarlo:

```bash
python scripts/build_clean_catalog.py --write --check-gcs
```

## Output artifact (publication)

Il clean parquet pubblico è raggiungibile come:

```text
gs://dataciviclab-clean/{slug}/*/{slug}_*_clean.parquet
```

L'MCP risolve automaticamente i blob GCS pubblici senza necessitare di autenticazione.
