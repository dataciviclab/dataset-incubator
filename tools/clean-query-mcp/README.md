# Clean Query MCP

Server MCP sperimentale, read-only, per interrogare i clean parquet pubblici del DataCivicLab tramite DuckDB.

Questo tool vive in `dataset-incubator` perché il contratto dei clean ufficiali nasce qui. Il catalogo letto dal server è:

```text
registry/clean_catalog.json
```

Il file locale `datasets.yml` non è più fonte di verità. Il catalogo MCP deve derivare dal Lab Clean Registry.

## Tool

| Tool | Scopo |
|---|---|
| `list_datasets()` | Lista slug disponibili |
| `describe_dataset(slug)` | Schema completo: colonne, tipi, ruolo, periodo |
| `run_query(sql, dataset, max_rows, year)` | Query DuckDB read-only sul parquet clean |
| `cache_stats()` | Stato della cache di risoluzione GCS |

## Runtime locale

Nel workspace DataCivicLab il runtime canonico è la venv del toolkit:

```bash
/home/gabry/dev/dataciviclab-workspace/toolkit/.venv/bin/python -m pip install -r /home/gabry/dev/dataciviclab-workspace/dataset-incubator/tools/clean-query-mcp/requirements.txt
```

Config MCP:

```json
{
  "mcpServers": {
    "clean-query": {
      "command": "/home/gabry/dev/dataciviclab-workspace/toolkit/.venv/bin/python",
      "args": [
        "/home/gabry/dev/dataciviclab-workspace/dataset-incubator/tools/clean-query-mcp/server.py"
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

## Smoke test

```bash
/home/gabry/dev/dataciviclab-workspace/toolkit/.venv/bin/python tools/clean-query-mcp/scripts/smoke.py
```

Limitato a un dataset:

```bash
/home/gabry/dev/dataciviclab-workspace/toolkit/.venv/bin/python tools/clean-query-mcp/scripts/smoke.py --dataset ispra_ru_base
```

## Limiti noti

- Il tool interroga un dataset alla volta.
- Le analisi cross-dataset richiedono una preparazione a monte o un’estensione esplicita del contratto.
- Il catalogo semantico resta manuale finché non verrà generato direttamente dai `dataset.yml` e dai run record DI.
