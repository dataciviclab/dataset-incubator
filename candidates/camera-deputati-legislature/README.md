# Camera Deputati — Legislature

## Domanda

Quanti deputati hanno fatto parte di ciascuna legislature della Camera?

## Fonte

[dati.camera.it/sparql](https://dati.camera.it/sparql) — endpoint SPARQL del Catalogo linked-data Camera dei deputati.

## Perimetro

Tutti i deputati di tutte le legislature della Repubblica Italiana (fino alla XIX). Ogni deputato può comparire in più legislature — la chiave è `(deputato, legislature)`.

## Schema

| Colonna | Tipo | Descrizione |
|---|---|---|
| `deputato` | string | URI RDF del deputato |
| `cogn` | string | Cognome |
| `nome` | string | Nome |
| `legislatura` | string | Numero della legislature (es. "17", "18", "19") |
| `gender` | string | Sesso |

## Output

- **Raw**: CSV da SPARQL, paginazione automatica (3 pagine × 10k)
- **Clean**: raw-faithful, 27.764 righe, 5 colonne
- **Mart**: `mart_deputati.parquet` — un record per `(deputato, legislature)`

## Note tecniche

- L'estrazione della legislature avviene dall'URI `?leg` (`repubblica_N`) tramite `REPLACE`
- Il WAF della Camera blocca risposte >10k righe — risolto con `pages: 3` nel dataset.yml
- Endpoint SPARQL puo' restituire 503 in modo intermittente

## Run

```bash
cd dataset-incubator
python -m toolkit.cli.app run all \
  --config candidates/camera-deputati-legislature/dataset.yml --years 2024
```
