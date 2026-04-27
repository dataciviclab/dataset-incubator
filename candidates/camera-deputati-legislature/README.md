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

## Output atteso

- **Raw**: CSV da SPARQL con 10k+ righe
- **Clean**: raw-faithful, nessun filtro
- **Mart**: `mart_deputati.parquet` — un record per `(deputato, legislature)`, unico per deputato per legislature

## Note tecniche

- L'estrazione della legislature avviene dall'URI `?leg` (`repubblica_N`) tramite `REPLACE(STR(?leg), 'http://dati.camera.it/ocd/legislatura.rdf/repubblica_', '')`
- `dct:title` non è disponibile su quel endpoint — la legislature è solo nell'URI
- L'endpoint SPARQL Camera può restituire 503 in modo intermittente

## Run

```bash
cd toolkit
python -m toolkit.cli.app run all \
  --config ../dataset-incubator/candidates/camera-deputati-legislature/dataset.yml
```
