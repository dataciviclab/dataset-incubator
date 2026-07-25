# ANAC — Certificazione Collaudo

**Dataset**: `anac_collaudo`
**Fonte**: ANAC — Autorità Nazionale Anticorruzione, [dati.anticorruzione.it](https://dati.anticorruzione.it/opendata/dataset/collaudo)
**Licenza**: CC BY-SA 4.0

## Contenuto

Certificazioni di collaudo (o regolare esecuzione) degli appalti ordinari. Ogni riga rappresenta il collaudo finale di un contratto, con esito positivo/negativo, date e riserve.

## Schema

| Colonna | Tipo | Descrizione |
|---|---|---|
| `cig` | VARCHAR | Chiave — join con `anac_bandi_gara` |
| `data_delibera` | DATE | Data delibera collaudo |
| `data_cert_collaudo` | DATE | Data certificato collaudo |
| `esito_collaudo` | VARCHAR | POSITIVO / NEGATIVO |
| `data_inizio_oper` | DATE | Data inizio operatività |
| `data_regolare_esec` | DATE | Data regolare esecuzione |
| `data_nomina_coll` | DATE | Data nomina collaudatore |
| `data_collaudo_stat` | DATE | Data collaudo statico (solo lavori) |
| `id_aggiudicazione` | BIGINT | Join con `anac_aggiudicazioni` |
| `riserve_avanzate` | DOUBLE | Riserve avanzate (€) |
| `riserve_definite` | DOUBLE | Riserve definite (€) |
| `importo_contenz_risolto` | DOUBLE | Importo contenzioso risolto (€) |

## Copertura

| Metrica | Valore |
|---|---|
| Righe | ~649k |
| CIG distinti | ~649k |
| Collaudi positivi | 98.6% |
| Peso CSV zippato | ~12 MB |
