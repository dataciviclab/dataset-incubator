# anpr-mobilita-residenziale

**Domanda guida:** Chi si sposta tra regioni in Italia? Il controesodo post-Covid è reale?

**Fonte:** ANPR — Anagrafe Nazionale della Popolazione Residente (Dipartimento per la Trasformazione Digitale, PCM)
**URL:** https://github.com/italia/anpr-opendata
**Formato:** CSV, 7 colonne, ~800 KB
**Copertura:** aprile 2022 – giugno 2026
**Licenza:** CC0

## Schema (7 colonne)

| Colonna | Tipo | Descrizione |
|---|---|---|
| `anno` | INTEGER | Anno |
| `mese` | INTEGER | Mese (1-12) |
| `partenza` | VARCHAR | Regione di provenienza |
| `cod_regione_partenza` | VARCHAR | Codice ISTAT regione partenza |
| `arrivo` | VARCHAR | Regione di destinazione |
| `cod_regione_arrivo` | VARCHAR | Codice ISTAT regione arrivo |
| `totale` | INTEGER | Numero trasferimenti di residenza |

## Mart

- **`mart_saldi_regionali`** — arrivi, partenze, saldo netto, flussi interni e quota interni per regione × anno. Include ESTERO.
- **`mart_corridoi`** — trasferimenti per coppia origine → destinazione × anno. Include ESTERO.
- **`mart_trend_mensile`** — totale trasferimenti per anno × mese con quota % sul totale annuo.

Rispondono alle 13 domande della [discussion #393](https://github.com/orgs/dataciviclab/discussions/393) (saldi, corridoi Sud→Nord, stagionalità, ESTERO).

## Esecuzione

```bash
cd dataset-incubator
toolkit run -c candidates/anpr-mobilita-residenziale/dataset.yml
```

## Issue di riferimento

- Intake: [#554](https://github.com/dataciviclab/dataset-incubator/issues/554)
