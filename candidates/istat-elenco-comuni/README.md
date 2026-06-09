# ISTAT elenco comuni — codici, superficie, catasto

## Dataset

Elenco completo dei comuni italiani (7.894) con codici ISTAT, codici catastali (Belfiore), superficie territoriale, popolazione e caratteristiche geografiche.

- **fonte**: ISTAT SITUAS via [opensituas](https://github.com/ondata/opensituas)
- **report SITUAS**: 61 (codici + catasto), 74 (superficie + popolazione), 73 (zona altimetrica)
- **snapshot**: 09 giugno 2026
- **copertura**: tutti i 7.894 comuni italiani

## Perché vale la pena averlo

È un support dataset ad alto impatto cross-analisi. Serve a:

- **normalizzare per superficie** (densità) — rifiuti/km², consumo suolo, popolazione per km², housing
- **join con dataset fiscali** — INPS pensioni e stipendi, IRPEF, IMU usano codici catastali
- **join con dataset sanitari, giudiziari, PA** — la maggior parte dei dataset pubblici italiani ha granularità comunale e usa codice ISTAT

Al momento il Lab non aveva superficie comunale né mapping codice catastale ↔ ISTAT in formato queryabile.

## Output minimo

- **clean**: parquet con codice_istat, denominazione, codice_catastale, superficie_km², popolazione, regione, provincia, zona altimetrica, altitudine, litoraneità
- **mart_superficie**: codice_istat + denominazione + km² per join rapidi
- **mart_codici_catastali**: mapping codice ISTAT ↔ codice catastale (Belfiore)

## Stato

- intake — PR [#487](https://github.com/dataciviclab/dataset-incubator/pull/487)

## Prossimo passo

- validare su CI e mergiare
- agganciare ad analisi esistenti (INPS stipendi, rifiuti, consumo suolo) per dimostrare utilità reale
