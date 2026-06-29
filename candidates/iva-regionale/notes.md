# Notes — iva-regionale

## Stato

Candidate v0. Vista Regione (CIVATOT0201) per 5 anni (2020-2024).

## Copertura

| Anno d'imposta | Anno presentazione | Righe |
|:--------------:|:------------------:|:-----:|
| 2019 | 2020 | 23 |
| 2020 | 2021 | 23 |
| 2021 | 2022 | 23 |
| 2022 | 2023 | 23 |
| 2023 | 2024 | 23 |

## Anni disponibili (per espansione)

Tutti gli anni dal 2009 al 2024 funzionano (16 anni totali).

## Note tecniche

- `TOOLKIT_ALLOW_SCRIPT_SOURCE=1` necessario per il preprocess
- preprocess.py scarica, salta metadati, normalizza formato numerico italiano
- I valori raw sono in migliaia di euro; il clean moltiplica ×1000 per avere euro
- `***` = data masking (meno di 3 contribuenti) → NULL

## Viste disponibili (per v1)

- 0201: Regione (fatta)
- 0202: Settore ATECO (lettera)
- 0203: Classe volume d'affari
- 0204: Tipo soggetto
