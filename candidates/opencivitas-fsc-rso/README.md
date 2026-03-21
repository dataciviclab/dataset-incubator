# opencivitas-fsc-rso

Candidate multi-source - Fondo di Solidarità Comunale 2025 per i Comuni delle
Regioni a Statuto Ordinario.

## Stato

`incubating` - candidate aperto da [#85](https://github.com/dataciviclab/dataset-incubator/issues/85),
nato dalla Discussion [#75](https://github.com/dataciviclab/dataset-incubator/discussions/75).

## Domanda

I comuni con capacità fiscale più bassa ricevono davvero più risorse
perequative in proporzione, oppure la dotazione finale FSC 2025 redistribuisce
in modo meno intuitivo del previsto?

## Dataset

Nucleo multi-source OpenCivitas FSC 2025.

Fonti previste nel v0:

| ID | Fonte | Ruolo | Stato |
|---|---|---|---|
| A | FSC 2025 variabile-valore | base principale con componenti di calcolo per comune | `run all` verde |
| B | Metadati enti FSC 2025 | mapping `USERNAME -> comune/provincia/regione` | `run all` verde |

Perimetro iniziale volutamente stretto:

- solo `2025`
- solo RSO
- primo asse pulito nel source `A`
- primo mapping anagrafico nel source `B`
- prossimo passo: join minimo leggibile con poche componenti chiave:
  - `POPOLAZIONE`
  - `CAPACITA_FISCALE`
  - `FONDO_PEREQUATIVO`
  - `DOTAZIONE_FINALE_FSC`
  - `IMU_TASI_STANDARD`
  - `TOTALE_RISORSE_STORICHE`

## Perché vale la pena testarlo

- si aggancia in modo naturale alle Discussion DCL `#91` e `#114`
- aggiunge il meccanismo di calcolo del FSC alle letture già fatte sui
  trasferimenti correnti
- entrambe le fonti del v0 sono accessibili e leggibili senza scraping
- la struttura multi-source evita di trattare i metadati come follow-up esterno
  a un join che è già parte costitutiva del candidate

## Output minimo atteso

- `sources/a_fsc_2025` verde
- `sources/b_enti_2025` verde
- primo join leggibile per comune come step successivo del candidate

## Criterio di promozione

- [x] source `A` eseguibile
- [x] source `B` eseguibile
- [ ] join minimo leggibile tra `A` e `B`
- [ ] lettura v0 con almeno un output o notebook prudente
- [ ] decisione se entra in `dataciviclab/preanalysis`
