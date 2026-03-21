# b_enti_2025

Source `B` - metadati enti FSC 2025 per il mapping `USERNAME -> comune`.

## Stato

`incubating` - sorgente interna del candidate
[opencivitas-fsc-rso](../../README.md), nata durante il lavoro su
[#85](https://github.com/dataciviclab/dataset-incubator/issues/85).

## Uso previsto

Decodificare la chiave tecnica `USERNAME` presente nei file OpenCivitas FSC 2025 e
agganciare:

- denominazione comune
- provincia
- regione

## Dataset

Fonte principale:

- OpenCivitas / Sogei, metadati enti FSC 2025
- file:
  `https://docs.opencivitas.it/Metadati_Enti_FSC_2025_xlsx.zip`
- workbook: `Metadati_Enti_FSC_2025.xlsx`
- sheet: `anagrafica_enti2025`

## Output minimo atteso

- `clean` sul workbook XLSX
- `mart` con una riga per `USERNAME`
- mapping riusabile per il join con `opencivitas-fsc-rso`

## Ruolo nel candidate

- fornire il mapping di base per il join con il source `A`
- evitare che il candidate principale resti bloccato su chiavi tecniche non
  leggibili
