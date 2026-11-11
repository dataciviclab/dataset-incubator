# Note tecniche — istat-cittadinanze

## Fonte e canale

| | |
|---|---|
| Dataflow | `IT1 / 29_849` — Acquisitions of citizenship (v1.0) |
| Canale | `type: sdmx` (endpoint esploradati) |
| Filtri | `FREQ=A`, `DATA_TYPE=ACQCITIZ`, `SEX=9` (totale), `AGE=TOTAL` |
| Grano | anno × territorio × ex-cittadinanza × processo di acquisizione |
| Anni | 2012–2025 |

## Perché SDMX e non DBnomics

Il mirror DBnomics è **fermo al 2023** (ultimo indice 2024-10), mentre la fonte
ISTAT espone già 2024 e 2025. Il plugin `sdmx` fa **una sola richiesta** e
normalizza in CSV lungo (~494 serie/anno × 14 anni = 6.923 righe, ~2 min).
Il vecchio canale `dbnomics` non è più utilizzabile per aggiornare il dataset.

## Freschezza e revisioni

- I dati 2024–2025 possono essere rivisti da ISTAT nei rilasci successivi.
- Cross-check: totale 2023 = **213.567**, identico a Eurostat `MIGR_ACQ`.
- Il totale nazionale non è la somma dei paesi: il dettaglio per ex-cittadinanza
  copre solo 10 paesi (più `WORLD`), quindi la somma è parziale (2025: 193.380
  su 196.955).

## Scelte di modellazione

- `livello` è derivato dalla lunghezza del codice territoriale (`IT`=nazionale,
  3=ripartizione, 4=regione, 5=provincia) — euristica documentata.
- `aggregato` marca le righe che non sono foglie (macro-aree, `WORLD`, aree
  geopolitiche): serve a evitare doppi conteggi.
- I nomi di territori e cittadinanze vengono da codelist locali
  (`codelists/istat_territori.csv`, `codelists/istat_cittadinanze.csv`).
- `years: [2026]` è l'anno nominale del run (path output stabile); la copertura
  reale è dichiarata in `time_coverage`.

## Chiave

`clean.validate.primary_key = [anno, territorio_codice, cittadinanza_codice,
processo_codice]` — verificata senza duplicati sul clean (6.923 righe).
