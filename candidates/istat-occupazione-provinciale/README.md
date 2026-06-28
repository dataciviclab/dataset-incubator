# istat-occupazione-provinciale

**Domanda guida:** Come si distribuisce il tasso di occupazione tra le province italiane? Il divario Nord-Sud sta aumentando o diminuendo?

**Fonte:** ISTAT — SDMX dataflow `150_915` (Tasso di occupazione, DCCV_TAXOCCU1)
**Accesso:** Endpoint HVD ISTAT, SDMX-CSV diretto
**Licenza:** CC BY (ISTAT)
**Granularità:** provincia (NUTS3)
**Copertura:** 2018–2025 (8 anni, serie provinciale completa)

## Schema clean (9 colonne)

```
ref_area      VARCHAR  — Codice NUTS3 provincia (es. ITC45)
territorio    VARCHAR  — Nome provincia (es. Milano)
anno          INTEGER  — Anno (2004–2025)
indicatore    VARCHAR  — EMP_R (tasso occupazione)
sesso_codice  VARCHAR  — 1=maschi, 2=femmine, 9=totale
sesso         VARCHAR  — maschi / femmine / totale
eta_codice    VARCHAR  — Codice classe età (es. Y15-64)
eta           VARCHAR  — Classe età (es. 15-64 years)
valore        DOUBLE   — Tasso di occupazione % (0–100)
```

## Esecuzione

```bash
cd dataset-incubator
python -m toolkit.cli.app run full \
  --config candidates/istat-occupazione-provinciale/dataset.yml
```

## Issue di riferimento

- Intake: [#556](https://github.com/dataciviclab/dataset-incubator/issues/556)
