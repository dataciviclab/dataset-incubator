# Popolazione ISTAT comunale

## Tipo

**Support dataset** — base infrastrutturale per join, coverage check, indicatori pro capite.

## Fonte

ISTAT — demo.posas `POSAS_{year}_it_Comuni.zip`
URL: `https://demo.istat.it/data/posas/POSAS_{year}_it_Comuni.zip`
Formato: ZIP → CSV, `;` delim, `utf-8` con BOM. Skip 1 riga (header doppio).

## Schema

**Clean**: 20 colonne — raw-faithful, rinomine a snake_case.

**Mart `popolazione_by_comune`**: `[anno_riferimento, codice_comune, comune, popolazione_residente, popolazione_maschile, popolazione_femminile]` — un record per comune, ETA=999.

**Mart `popolazione_by_eta`**: `[anno_riferimento, codice_comune, comune, eta, popolazione_residente, popolazione_maschile, popolazione_femminile]` — un record per comune per classe di età (0-100).

Chiave di join: `codice_comune`

## Copertura

| Anno | Comuni | Popolazione |
|---|---|---|
| 2019 | 7.954 | 59.816.673 |
| 2020 | 7.914 | 59.641.488 |
| 2021 | 7.903 | 59.236.213 |
| 2022 | 7.904 | 59.030.133 |
| 2023 | 7.901 | 58.997.201 |
| 2024 | 7.900 | 58.971.230 |
| 2025 | 7.896 | 58.943.464 |

## QC

- Clean = Raw per tutti i 7 anni (nessun filtro) ✅
- Maschi + Femmine = Popolazione su tutti gli anni ✅
- Nessun comune senza nome o con pop=0 ✅
- by_comune vs sum(by_eta): differenza = 0 ✅

## Uso

- join con dataset comunali (es. IRPEF)
- controlli coverage territoriale
- indicatori pro capite
- detector anomalie territoriali

## Stato

`runnable` — tutti e 7 gli anni con raw, clean, mart verificati.
