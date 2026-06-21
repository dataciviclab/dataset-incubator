# opencivitas-fsc-rso

Candidate single-source con support — Fondo di Solidarietà Comunale per i
Comuni delle Regioni a Statuto Ordinario. **Multi-anno: 2022–2025.**

## Stato

`incubating` — candidate nato da [#85](https://github.com/dataciviclab/dataset-incubator/issues/85),
derivato dalla Discussion [#75](https://github.com/dataciviclab/dataset-incubator/discussions/75).

## Domanda

I comuni con capacità fiscale più bassa ricevono davvero più risorse
perequative in proporzione, oppure la dotazione finale FSC redistribuisce
in modo meno intuitivo del previsto? E come cambia la distribuzione tra 2022 e 2025?

## Dataset

Struttura: candidate principale con support per geografia.

| ID | Fonte | Ruolo | Stato |
|---|---|---|---|
| A | FSC {year} variabile-valore | candidate: base principale | ✅ anni 2022–2025 |
| B | Metadati enti FSC | support: mapping `USERNAME -> geografia comune` | ✅ fisso (2025) |

Perimetro:

- **2022–2025** (4 annualità)
- solo RSO (Regioni a Statuto Ordinario)
- pivot FSC (EAV→wide) + join geografia da support nel CLEAN
- output CLEAN: 13 colonne wide (include `anno`)

## Anni

| Anno | Comuni | Fonte | Note |
|:----:|:-----:|-------|------|
| 2022 | 6.581 | OpenCivitas | Colonna: VAR_FSC_NAME / VAR_FSC_VAL |
| 2023 | 6.578 | OpenCivitas | Colonna: VAR_FSC_NAME / VAR_FSC_VAL |
| 2024 | 6.578 | OpenCivitas | Colonna: VAR_FSC_NAME / VAR_FSC_VAL |
| 2025 | 6.573 | OpenCivitas | Colonna: Componenti di calcolo del fondo / Valore |

Il clean SQL gestisce entrambi i formati raw (colonne per posizione).

## Output minimo atteso

- [x] candidate eseguibile (RAW → CLEAN → MART)
- [x] mart table `mart_compose_comuni` con join 100%
- [x] notebook v0 verificato