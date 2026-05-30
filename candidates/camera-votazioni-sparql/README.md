# Camera Votazioni — Legislature XVIII e XIX

## Domanda

Quante votazioni ci sono state alla Camera dei deputati, con che esito, e come hanno votato i gruppi parlamentari?

## Fonte

[dati.camera.it/sparql](https://dati.camera.it/sparql) — endpoint SPARQL del Catalogo linked-data Camera dei deputati.

## Perimetro

Tutte le votazioni della Camera dal 2018 a oggi (XVIII e XIX legislatura). Ogni riga è una votazione con esito, conteggi, e metadata.

## Schema

| Colonna | Tipo | Descrizione |
|---|---|---|
| `favorevoli` | int | Voti favorevoli |
| `contrari` | int | Voti contrari |
| `astenuti` | int | Astenuti |
| `votanti` | int | Totale votanti |
| `presenti` | int | Totale presenti in Aula |
| `approvato` | bool | Esito (approvato/non approvato) |
| `votazione_finale` | bool | Votazione finale su un atto |
| `votazione_segreta` | bool | Votazione segreta |
| `richiesta_fiducia` | bool | Questione di fiducia |
| `titolo` | string | Oggetto della votazione |
| `maggioranza` | int | Quorum richiesto |
| `data` | date | Data della votazione |
| `legislatura` | string | URI della legislatura |
| `seduta` | string | URI della seduta |
| `atto_camera` | string | URI dell'atto collegato |

## Note tecniche

- Ogni anno e' una query separata con filtro `STRSTARTS(?data, "{year}")`
- Il WAF della Camera blocca risposte >10k righe — la suddivisione per anno evita il problema
- Anni completi: 2018-2025

## Run

```bash
cd dataset-incubator
python -m toolkit.cli.app run all \
  --config candidates/camera-votazioni-sparql/dataset.yml --years 2024
```
