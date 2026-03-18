# Notes — ispra-consumo-suolo

## Stato

Scaffold v0 creato (Marzo 2026).
Pipeline non ancora eseguita — da verificare lettura XLSX.

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

## Colonne nel mart_comuni

| Campo | Descrizione |
|---|---|
| pro_com | Codice ISTAT comune (6 cifre) |
| comune | Nome comune |
| provincia | Nome provincia |
| regione | Nome regione |
| incremento_ha_2023_2024 | Incremento netto consumo suolo 2023-2024 [ha] |
| stock_ha_2024 | Suolo consumato cumulato 2024 [ha] |
| stock_pct_2024 | Suolo consumato 2024 [% superficie] |

## Issue di riferimento

- dataset-incubator #32 — intake originale
