# ANAC — Stati di Avanzamento Lavori (SAL)

**Dataset**: `anac_stati_avanzamento`
**Fonte**: ANAC — Autorità Nazionale Anticorruzione, [dati.anticorruzione.it](https://dati.anticorruzione.it/opendata/dataset/stati-avanzamento)
**Licenza**: CC BY-SA 4.0

## Contenuto

Stati di Avanzamento Lavori (SAL) degli appalti ordinari. Ogni SAL rappresenta una tranche di pagamento in corso d'opera, con importo, date e scostamenti rispetto al cronoprogramma.

## Schema

| Colonna | Tipo | Descrizione |
|---|---|---|
| `cig` | VARCHAR | Chiave — join con `anac_bandi_gara` |
| `denominazione_sal` | VARCHAR | Descrizione SAL (es. "1 STATO AVANZAMENTO LAVORO") |
| `flag_ritardo` | VARCHAR | IN LINEA / IN RITARDO / IN ANTICIPO |
| `data_emissione_sal` | DATE | Data emissione SAL |
| `importo_sal` | DOUBLE | Importo del SAL (€) |
| `n_giorni_scostamento` | INTEGER | Giorni di scostamento dal cronoprogramma |
| `progressivo_sal` | INTEGER | Numero progressivo del SAL |
| `id_aggiudicazione` | BIGINT | Join con `anac_aggiudicazioni` |
| `data_cert_pagamento` | DATE | Data certificato di pagamento |
| `importo_cert_pagamento` | DOUBLE | Importo certificato di pagamento (€) |
| `giorni_proroga` | DOUBLE | Giorni di proroga concessi |

## Copertura

| Metrica | Valore |
|---|---|
| Righe | ~1.27M |
| CIG distinti | ~344k |
| Peso CSV zippato | ~30 MB |
