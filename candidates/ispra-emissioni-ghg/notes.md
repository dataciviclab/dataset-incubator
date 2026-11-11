## Tecnico

- Fonte: ISPRA — Indicatori Ambientali (XLSX)
- URL: non stabile (data di pubblicazione nel path). Rilascio corrente `/2026-06-11/`
  `Tabella 1 Emissioni_gas_serra_da_processi_energetici_1990_2024_0.xlsx`
- Encoding: utf-8 (CSV convertito), delim: `;`
- Granularità: nazionale (nessuna disaggregazione regionale)
- Periodo: 1990-2024 (35 anni)
- Join key: anno

## Cambio formato 2025 → 2026

Il rilascio 2026 (dati 1990-2024) **non è solo un anno in più**:

| | rilascio 2025 (dati 1990-2023) | rilascio 2026 (dati 1990-2024) |
|---|---|---|
| Formato | `.xls` (old) | `.xlsx` |
| Foglio dati | `D03_027` (sheet 0) | `Dati` |
| Colonna 3 | `Residenziale e servizi` | `Terziario e Residenziale + Agricoltura e Pesca` |
| Righe | 34 (1990-2023) | 35 (1990-2024) |

`preprocess.py` legge il foglio `Dati` per **posizione** (colonne 0..5) e mantiene
i nomi di output storici (`residenziale_e_servizi`), così `clean.sql` e i mart
restano invariati. La terza colonna ha però un perimetro più ampio: il confronto
2023 vs 2024 è omogeneo, il confronto con versioni precedenti del dataset no.

**Revisione della serie**: l'inventario ISPRA ricalcola l'intera serie a ogni
rilascio. I valori 1990-2023 possono quindi differire da quelli pubblicati in
precedenza (qui: totale 1990 = 426,2 Mt).

## Preprocessing

Lo script `preprocess.py`:
1. Scarica l'XLSX
2. Legge il foglio `Dati`
3. Salta le 2 righe di header (header + unità di misura)
4. Produce CSV con header normalizzati (`anno;industrie_energetiche;...;totale`)

Per aggiornare i dati: `python preprocess.py raw_input.csv`
A ogni nuovo rilascio va aggiornato `RELEASE_URL` in `preprocess.py`.

## Analitico

Trend chiave 1990→2024:
- Industrie energetiche: 151,9 → 68,3 Mt (-55%)
- Industrie manifatturiere: 92,2 → 46,2 Mt (-50%)
- Terziario/residenziale + agricoltura: 78,9 → 66,2 Mt (-16%)
- Trasporti: 103,3 → 113,9 Mt (+10%)
- Totale: 426,2 → 294,5 Mt (-31%)

Il calo più marcato è nelle industrie energetiche (+ manifatturiere). I trasporti
sono l'unico settore in crescita. Il crollo del 2020 è stato recuperato solo in
parte: nel 2024 le emissioni energetiche sono -3,5% sul 2023.

## Cautele

- Copre solo processi energetici (~81% delle emissioni totali italiane nel 2024)
- Esiste un secondo indicatore ISPRA complementare (emissioni totali per gas) — possibile estensione
- I dati sono annuali (non mensili/trimestrali)
- Per analisi regionali servono altre fonti (es. inventario regionale ISPRA)
