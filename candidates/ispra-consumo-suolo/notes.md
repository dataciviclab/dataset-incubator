# Notes — ispra-consumo-suolo

## Stato

Scaffold v0 creato (Marzo 2026).
Pipeline eseguita con lettura XLSX verificata.
Issue tecnica aperta: estrazione completa della serie incrementi per periodo (`#70`).

## Esecuzione

```
cd dataset-incubator
toolkit/.venv/Scripts/python.exe -m toolkit.cli.app run all \
  --config candidates/ispra-consumo-suolo/sources/a_consumo_suolo/dataset.yml
```

## Struttura XLSX ISPRA

- File: `consumo_di_suolo_estratto_dati_2025_anni_2006_2024.xlsx`
- Foglio target: `Comuni_2006_2024`
- La riga 1 (dopo header) potrebbe contenere unita di misura — filtrata in clean.sql

## Colonne chiave nel mart_comuni

| Campo | Descrizione |
|---|---|
| pro_com | Codice ISTAT comune (6 cifre) |
| comune | Nome comune |
| provincia | Nome provincia |
| regione | Nome regione |
| incremento_ha_2023_2024 | Incremento netto consumo suolo 2023-2024 [ha] |
| incremento_netto_ha_<periodo> | Serie degli incrementi netti per periodo ISPRA [ha] |
| incremento_lordo_ha_<periodo> | Serie degli incrementi lordi per periodo ISPRA [ha] |
| stock_ha_2024 | Suolo consumato cumulato 2024 [ha] |
| stock_pct_2024 | Suolo consumato 2024 [% superficie] |

### Periodi disponibili

- `2006_2012`
- `2012_2015`
- `2015_2016`
- `2016_2017`
- `2017_2018`
- `2018_2019`
- `2019_2020`
- `2020_2021`
- `2021_2022`
- `2022_2023`
- `2023_2024`

## Issue di riferimento

- dataset-incubator #32 — intake originale
- dataset-incubator #70 — estensione serie incrementi 2006-2024
