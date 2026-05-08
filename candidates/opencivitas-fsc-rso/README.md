# opencivitas-fsc-rso

Candidate single-source con support — Fondo di Solidarietà Comunale 2025 per i
Comuni delle Regioni a Statuto Ordinario.

## Stato

`incubating` — candidate nato da [#85](https://github.com/dataciviclab/dataset-incubator/issues/85),
derivato dalla Discussion [#75](https://github.com/dataciviclab/dataset-incubator/discussions/75).

## Domanda

I comuni con capacità fiscale più bassa ricevono davvero più risorse
perequative in proporzione, oppure la dotazione finale FSC 2025 redistribuisce
in modo meno intuitivo del previsto?

## Dataset

Struttura: candidate principale con support per geografia.

| ID | Fonte | Ruolo | Stato |
|---|---|---|---|
| A | FSC 2025 variabile-valore | candidate: base principale | ✅ mart `mart_compose_comuni` |
| B | Metadati enti FSC 2025 | support: mapping `USERNAME -> geografia comune` | ✅ in `support_datasets/opencivitas-fsc-enti-rso/` |

Perimetro iniziale:

- solo `2025`
- solo RSO
- metriche FSC pivot per comune con join geografia da support
- output: `mart_compose_comuni.parquet` (6573 comuni RSO, 15 colonne)

## Output minimo atteso

- [x] candidate eseguibile (RAW → CLEAN → MART)
- [x] mart table `mart_compose_comuni` con join 100%
- [X] notebook v0 verificato