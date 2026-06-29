# iva-regionale

**Domanda guida:** Come si distribuisce il volume d'affari IVA tra le regioni italiane?

**Fonte:** MEF — Dipartimento delle Finanze
**URL:** https://www1.finanze.gov.it/finanze/analisi_stat/public/index.php
**Dataset:** CIVATOT0201 (Regione)
**Formato:** CSV con 7 righe metadati → normalizzato da preprocess
**Copertura:** 2014–2023 (10 anni, anno d'imposta)
**Nota:** L'URL MEF usa l'anno di presentazione (es. `2024CIVATOT0201` = dichiarazioni 2024). Il clean converte in anno d'imposta sottraendo 1.
**Licenza:** CC BY (MEF)
**Valori:** in **euro** (convertiti da migliaia ×1000)

## Schema (9 colonne)

| Colonna | Tipo | Descrizione |
|---|---|---|
| `anno` | INTEGER | Anno d'imposta (URL anno - 1) |
| `regione` | VARCHAR | Denominazione regione |
| `cod_regione` | VARCHAR | Codice ISTAT regione |
| `contribuenti` | BIGINT | Numero contribuenti IVA |
| `volume_affari_eur` | DOUBLE | Volume d'affari (€) |
| `acquisti_eur` | DOUBLE | Acquisti e importazioni (€) |
| `va_fiscale_eur` | DOUBLE | Valore aggiunto fiscale (€) |
| `imposta_dovuta_eur` | DOUBLE | Imposta IVA dovuta (€) |
| `imposta_credito_eur` | DOUBLE | IVA a credito (€) |

## Esecuzione

```bash
cd dataset-incubator
TOOLKIT_ALLOW_SCRIPT_SOURCE=1 python -m toolkit.cli.app run all \
  --config candidates/iva-regionale/dataset.yml
```

## Issue di riferimento

- Intake: [#551](https://github.com/dataciviclab/dataset-incubator/issues/551)
