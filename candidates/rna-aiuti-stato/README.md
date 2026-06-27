# RNA — Aiuti di Stato alle imprese

**Fonte**: [Registro Nazionale Aiuti di Stato](https://www.rna.gov.it/open-data) (MIMIT)
**Repo**: [dataciviclab/rna-aiuti-stato](https://github.com/dataciviclab/rna-aiuti-stato)
**Stato**: completato (10/10 anni, ~17 milioni di righe)

Ogni aiuto pubblico concesso alle imprese italiane: beneficiario (CF e denominazione), importo, procedimento, settore NACE, regione, CUP. Dati dal 2017 al 2026.

La pipeline di trasformazione XML → Parquet è gestita dal repo `rna-aiuti-stato` (scripts/full_batch.py).
Questo candidate esiste per registrare il dataset nel catalogo Lab e per le query MART aggregate.

### Note

- **10 anni completati**: 2017-2026, ~17M righe, 704 MB parquet
- I parquet RAW sono su GCS (`gs://dataciviclab-clean/rna-aiuti-stato/`)
- Il push via CI è disabilitato (`auto_deploy`): il deploy avviene dal workflow `build` del repo
- I MART offrono aggregazioni per regione, procedimento e top beneficiari
- La pipeline con flush periodico (50k chunk) mantiene RAM sotto controllo
