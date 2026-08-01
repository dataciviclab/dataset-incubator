# RNA — Misure (leggi e regimi di aiuto)

**Fonte**: [Registro Nazionale Aiuti di Stato](https://www.rna.gov.it/open-data) (MIMIT)
**Repo**: [dataciviclab/rna-aiuti-stato](https://github.com/dataciviclab/rna-aiuti-stato)
**Stato**: completo (1994-2023, 12.874 misure)

Ogni legge, decreto o regime che autorizza aiuti di Stato in Italia. Collegabile agli aiuti via `car`.

La pipeline è gestita dal repo `rna-aiuti-stato` (scripts/full_batch.py --misure).
Questo candidate esiste per registrare il dataset nel catalogo Lab.

### Note

- Parquet unico su GCS (`gs://dataciviclab-clean/rna-aiuti-stato/misure/misure.parquet`)
- Il deploy su GCS avviene tramite CI di dataset-incubator (post-merge)
- **`car` non è unico**: la stessa misura ha più finestre di validità (es. car 1924 con periodo 2007-2021 e 2015-2030). PK = `car + data_inizio_misura`.

## Mart

| Mart | Descrizione |
|---|---|
| `mart_misure_per_tipo` | Conteggi e importi (prestiti garantiti + ad hoc) per tipo di misura |
| `mart_misure_attive` | Misure ancora attive per anno di istituzione |
| `mart_top_misure` | Top misure per importo totale, con stato attiva/scaduta |

Rispondono alla domanda D11 della [discussion #405](https://github.com/orgs/dataciviclab/discussions/405) (quali misure hanno erogato di più, misure dimenticate ma attive). NOTA: l'importo è il plafond della misura, non l'erogato effettivo (l'erogato si calcola dal join con `rna_aiuti_stato` via `car`).

## Esecuzione

```bash
cd dataset-incubator
toolkit run -c candidates/rna-misure/dataset.yml
```
