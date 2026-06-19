## Tecnico

- Fonte: ISPRA — Indicatori Ambientali (XLS)
- URL XLS: non stabile (data nel path `/2025-07-01/`)
- Encoding: utf-8 (CSV convertito), delim: `;`
- Granularità: nazionale (nessuna disaggregazione regionale)
- Periodo: 1990-2023 (34 anni)
- Join key: anno

## Preprocessing

Il file originale è un XLS (old format) con 2 sheet:
- Sheet 0 "D03_027": dati (riga 0=header, riga 1=sub-header unità, righe 2-35=dati)
- Sheet 1 "Metadati": titolo e fonte

Lo script `preprocess.py`:
1. Scarica l'XLS
2. Legge Sheet 0
3. Salta riga 1 (sub-header)
4. Produce CSV con header normalizzati in italiano

Per aggiornare i dati: `python preprocess.py raw_input.csv`

## Analitico

Trend chiave 1990→2023:
- Industrie energetiche: 152 → 80 Mt (-47%)
- Industrie manifatturiere: 92 → 50 Mt (-45%)
- Residenziale e servizi: 79 → 69 Mt (-13%)
- Trasporti: 103 → 109 Mt (+6%)
- Totale: 426 → 309 Mt (-27%)

Il calo più marcato è nelle industrie energetiche (+ manifatturiere). I trasporti sono l'unico settore sostanzialmente stabile (leggera crescita). Il crollo del 2020 è stato parzialmente recuperato.

## Cautele

- Copre solo processi energetici (~80% emissioni totali italiane)
- Esiste un secondo indicatore ISPRA complementare (emissioni totali per gas) — possibile estensione
- I dati sono annuali (non mensili/trimestrali)
- Per analisi regionali servono altre fonti (es. inventario regionale ISPRA)
