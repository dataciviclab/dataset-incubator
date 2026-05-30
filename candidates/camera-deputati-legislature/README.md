# Camera Deputati — Legislature

## Domanda

Quanti deputati hanno fatto parte di ciascuna legislature della Camera?

## Fonte

[dati.camera.it/sparql](https://dati.camera.it/sparql) — endpoint SPARQL del Catalogo linked-data Camera dei deputati.

## Perimetro

Tutti i deputati di tutte le legislature della Repubblica Italiana (fino alla XIX). Ogni deputato può comparire in più legislature — la chiave è `(deputato, legislature)`.

## Schema

| Colonna | Tipo | Descrizione |
|---|---|---|---|
| `deputato` | string | URI RDF del deputato |
| `cognome` | string | Cognome (da `foaf:surname` o `rdfs:label` per deputati storici) |
| `nome` | string | Nome (da `foaf:firstName` o `rdfs:label` per deputati storici) |
| `legislatura` | string | Codice legislature (es. "costituente", "regno_01", ..., "repubblica_19") |
| `gender` | string | Sesso (`male`/`female`/`null`) |

## Output

- **Raw**: CSV da SPARQL, paginazione automatica (3 pagine × 10k)
- **Clean**: 27.618 righe, 5 colonne, **99% nomi popolati**
- **Mart**: `mart_deputati.parquet` — un record per `(deputato, legislature)`

## Note tecniche

- I deputati della Repubblica hanno `foaf:surname` + `foaf:firstName`; quelli del Regno hanno solo `rdfs:label` nel formato "NOME COGNOME, Legislatura...". Il clean.sql unifica le due fonti.
- Il WAF della Camera blocca risposte >10k righe — risolto con `pages: 3, step: 10000` nel dataset.yml
- 9 righe su 27.618 (0.03%) non hanno nome — deputati con mandato senza dati anagrafici completi nel sistema
- Gender: popolato solo per deputati recenti (Repubblica) — storico ha `null`

## Run

```bash
cd dataset-incubator
python -m toolkit.cli.app run all \
  --config candidates/camera-deputati-legislature/dataset.yml --years 2024
```
