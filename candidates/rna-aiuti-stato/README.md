# RNA — Aiuti di Stato alle imprese

**Fonte**: [Registro Nazionale Aiuti di Stato](https://www.rna.gov.it/open-data) (MIMIT)
**Repo**: [dataciviclab/rna-aiuti-stato](https://github.com/dataciviclab/rna-aiuti-stato)
**Stato**: bootstrap in corso (6/10 anni completati)

Ogni aiuto pubblico concesso alle imprese italiane: beneficiario (CF e denominazione), importo, procedimento, settore NACE, regione, CUP.

La pipeline di trasformazione XML → Parquet è gestita dal repo `rna-aiuti-stato` (scripts/full_batch.py).
Questo candidate esiste per registrare il dataset nel catalogo Lab e per le query MART aggregate.

### Note

- I parquet RAW sono su GCS (`gs://dataciviclab-clean/rna-aiuti-stato/`)
- Il push via CI è disabilitato: il deploy avviene dal workflow `build` del repo
- I MART offrono aggregazioni per regione, procedimento e top beneficiari
