# anpr-mobilita-residenziale

**Domanda guida:** Chi si sposta tra regioni in Italia? Il controesodo post-Covid è reale?

**Fonte:** ANPR — Anagrafe Nazionale della Popolazione Residente (Dipartimento per la Trasformazione Digitale, PCM)
**URL:** https://github.com/italia/anpr-opendata
**Formato:** CSV, 7 colonne, ~98 KB
**Copertura:** aprile 2022 – settembre 2025
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

## Esecuzione

```bash
cd dataset-incubator
python -m toolkit.cli.app run full \
  --config candidates/anpr-mobilita-residenziale/dataset.yml
```

## Issue di riferimento

- Intake: [#555](https://github.com/dataciviclab/dataset-incubator/issues/555)
