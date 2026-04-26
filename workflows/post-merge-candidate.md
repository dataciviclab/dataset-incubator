---
name: post-merge-candidate
description: Checklist manuale per un maintainer dopo il merge di un candidate in dataset-incubator. Produce clean parquet in GCS.
license: MIT
metadata:
  version: "0.2"
  owner: "DataCivicLab"
  tags: [dataset-incubator, candidate, gcs, push]
---

# Workflow: post-merge-candidate

Workflow manuale da eseguire dopo il merge di una PR candidate in `dataset-incubator`.
Richiede accesso in scrittura a GCS (`dataciviclab-clean`).

## Quando eseguire

Dopo il merge di una PR che aggiunge o aggiorna un candidate in `candidates/{slug}/`.

## Step

### 1. Aggiorna il repo locale

```bash
git pull origin main
```

### 2. Runna il candidato con toolkit

```bash
cd dataset-incubator
toolkit run all --config candidates/{slug}/dataset.yml
# oppure per multi-source:
toolkit run all --config candidates/{slug}/sources/{source}/dataset.yml
```

Verifica che il run completi senza errori e che `out/data/clean/{slug}/` sia popolato.

### 3. Validazione (opzionale ma raccomandata)

```bash
toolkit validate all --config candidates/{slug}/dataset.yml
```

### 4. Push clean su GCS + BQ

```bash
python scripts/push_archive.py --layer clean --slug {slug} --create-bq-table --dry-run
```

Se il dry-run è ok, esegui per davvero:

```bash
python scripts/push_archive.py --layer clean --slug {slug} --create-bq-table
```

Il push include:
- parquet clean per ogni anno
- `pipeline_run.json` (traccia del run) accanto ad ogni anno
- external table BQ `dataciviclab.{slug}.clean` che punta ai file GCS

### 5. Aggiorna catalog **solo se serve**

```bash
# Controlla cosa cambierebbe prima di toccare il catalog
python scripts/build_clean_catalog.py --check-gcs
```

**Regola**: aggiorna il catalog solo se:
- è uno **slug nuovo** (non esiste ancora in `registry/clean_catalog.json`)
- oppure è cambiato il `multi_file` flag (da `false` a `true` o viceversa)
- oppure il GCS path è cambiato (es.vecchio `2024/file.parquet` → nuovo `*/file_*.parquet`)

**Non aggiornare** se:
- `multi_file: false` e lo slug già esiste con path corretto (il catalog è già allineato)
- solo il contenuto del parquet è cambiato (stesso path GCS, stesse colonne)

Se serve aggiornare:

```bash
python scripts/build_clean_catalog.py --write
git add registry/clean_catalog.json
git checkout -b chore/{slug}-postmerge-catalog
git commit -m "chore({slug}): aggiorna clean_catalog post-push GCS"
gh pr create --title "chore({slug}): aggiorna clean_catalog post-push GCS" --body "..."
```

### 6. Verifica

Il workflow `validate-clean-catalog` parte automaticamente dopo il push. Controlla che passi.

## Note

- Il mart non viene pushato in questo step — va fatto on-demand dopo analisi.
- Se il run fallisce per problemi di fonte (timeout, schema cambiato), apri issue nel repo prima di procedere.
- Il `pipeline_signals.json` si aggiorna automaticamente al merge via CI — non serve aggiornarlo manualmente.
- `--update-catalog` nel `push_archive.py` esegue un build automatico del catalog — usalo **solo** in combinazione con `--check-gcs` per verificare che serva davvero.
