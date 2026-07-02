# Clean Query MCP

Server MCP sperimentale, read-only, per interrogare i clean parquet pubblici del DataCivicLab tramite DuckDB.

## Tool (4)

### `find(query="", metric_only=False, limit=15)`

Scopre dataset per nome, descrizione, fonte e colonne.

```python
find("reddito")                      # 6 dataset con "reddito" in nome/desc/colonne
find("popolazione", metric_only=True)  # solo dataset con colonne numeriche
find()                                 # tutti i dataset
```

### `dataset_overview(slug, limit=10)`

Schema + conteggio righe + anteprima dati. `limit=0` per solo schema.

```python
dataset_overview("irpef_comunale")          # schema + count + 10 righe
dataset_overview("comuni_master", limit=0)  # solo schema, nessuna query DuckDB
```

### `dataset_graph(by_key="", by_dataset="", by_registry="")`

Mappa delle relazioni tra dataset. Legge `join_map.yaml` live.

```python
dataset_graph()                                    # mappa completa
dataset_graph(by_key="codice_istat")               # 13 dataset via ISTAT
dataset_graph(by_dataset="irpef_comunale")          # come si collega irpef
```

### `query(sql, datasets, dry_run=False, max_rows=100, year=None)`

Unico entry point per eseguire SQL. Supporta 1 o N dataset.

```python
# Singolo dataset
query("SELECT * FROM clean_input WHERE comune = 'Milano'",
      datasets=["irpef_comunale"])

# Cross-dataset (sostituisce cross_query)
query("SELECT i.*, p.popolazione FROM irpef_comunale i "
      "JOIN popolazione_istat_comunale p ON i.codice_istat_comune = p.codice_comune",
      datasets=["irpef_comunale", "popolazione_istat_comunale_2019_2025"])

# Explain senza eseguire (sostituisce explain_query)
query("SELECT COUNT(*) FROM clean_input", datasets=["irpef_comunale"], dry_run=True)
```

## Security

- Solo `SELECT` / `WITH`
- `max_rows` hard cap 500
- Keyword DDL/DML bloccate
- Scope enforcement: solo tabelle dichiarate in `datasets`
- `FROM 'url.parquet'` bloccato (string literal bypass)
- `dry_run` valida scope come modalità normale

## Runtime

```bash
pip install -e .
```

```json
{
  "mcpServers": {
    "clean-query": {
      "command": "clean-query-mcp"
    }
  }
}
```

## Smoke test

```bash
python -m tools.clean_query_mcp.scripts.smoke
python -m tools.clean_query_mcp.scripts.smoke --dataset ispra_ru_base
```

## Registry

- `registry/join_map.yaml` — relazioni tra dataset (fonte unica)
- `registry/clean_catalog.json` — catalogo dataset con schemi e path
