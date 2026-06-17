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

### Esplorazione semplificata

| Tool | Scopo |
|---|---|
| `dataset_overview(slug, limit)` | Panoramica completa: schema + conteggio righe + anteprima in una chiamata |
| `describe_dataset(slug)` | Schema completo: colonne, tipi, ruolo, periodo |

### Query diretta

| Tool | Scopo |
|---|---|
| `run_query(sql, dataset, max_rows, year)` | Query DuckDB read-only — solo SELECT/WITH, hard cap 500 righe |
| `explain_query(sql, dataset)` | Valida SQL senza eseguirla — stima validità e risolve parquet |

### Query e debug

| Tool | Scopo |
|---|---|
| `run_query(sql, dataset, max_rows, year)` | Query DuckDB read-only — solo SELECT/WITH, hard cap 500 righe |
| `explain_query(sql, dataset)` | Valida SQL senza eseguirla — stima validità e risolve parquet |
| `cache_stats()` | Stato della cache GCS — utile per debug

## Runtime

Da root del repository `dataset-incubator`:

```bash
pip install -e .
```

Config MCP:

```json
{
  "mcpServers": {
    "clean-query": {
      "command": "clean-query-mcp"
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

### Esplorazione iniziale

Dopo `toolkit run --config candidates/{slug}/dataset.yml` e push GCS:

```python
# 1. Panoramica completa (schema + conteggio + preview in un colpo)
dataset_overview(slug, limit=5)

# 2. Verifica valori chiave
run_query("SELECT DISTINCT regione FROM clean_input ORDER BY regione", slug)
```

### Analisi esplorativa

```python
# 1. Serie storica per dimensione
run_query("SELECT anno, regione, SUM(metric) AS value FROM clean_input GROUP BY anno, regione ORDER BY anno, regione", dataset)

# 2. Metriche aggregate
run_query("SELECT regione, SUM(metric) AS total FROM clean_input GROUP BY regione ORDER BY total DESC", dataset)

# 3. Query esplorativa
run_query("SELECT regione, SUM(...) FROM clean_input GROUP BY regione", dataset)
```

### Pre-publication (validazione)

Prima di aprire Discussion o promuovere su data-explorer:

```python
# 1. Quali dataset hanno metriche simili?
find_metric_datasets(metric_name='spesa')          # per cross-reference
column_search('regione')                            # per capire coverage

# 2. Valida query complessa prima di esporla
explain_query(sql, dataset)                         # senza eseguirla

# 3. Verifica copertura temporale
dataset_overview(slug)                              # period e total_rows
```

## Smoke test

```bash
python -m tools.clean_query_mcp.scripts.smoke
```

Limitato a un dataset:

```bash
python -m tools.clean_query_mcp.scripts.smoke --dataset ispra_ru_base
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
