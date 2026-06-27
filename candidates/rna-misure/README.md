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
- MART passthrough (nessuna aggregazione — dataset piccolo)
