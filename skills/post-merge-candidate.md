---
name: post-merge-candidate
description: Skill per il maintainer dopo il merge di un candidate in dataset-incubator. Run completo, push GCS, clean catalog.
license: MIT
metadata:
  version: "0.3"
  owner: "DataCivicLab"
  tags: [dataset-incubator, candidate, gcs, push, maintainer]
---

# Skill: post-merge-candidate

Skill per il maintainer dopo il merge di una PR candidate in `dataset-incubator`.
Richiede accesso in scrittura a GCS (`dataciviclab-clean`).

## Obiettivo

Clean parquet pubblicato in GCS, BQ table attiva, `clean_catalog.json` aggiornato, draft PR chiusa.

## Entry point

- PR mergiata su `candidates/` o `support_datasets/`
- Draft PR `chore(post-merge): aggiorna registry per PR #<num>` trovata tra le PR aperte

Il workflow `Post-Merge Candidate Registry` (`.github/workflows/post-merge-candidate.yml`) ha già fatto:
run CI + `pipeline_signals.json` aggiornato + draft PR aperta.

Se il run CI è fallito, usa gli artifact `sample-run-*` per diagnosticare prima di procedere.

## Procedura

### 1. Aggiorna repo

```bash
git pull origin main
```

### 2. Run completo

```bash
toolkit run all --config candidates/{slug}/dataset.yml
```

Copre tutti gli anni dichiarati nel config.

### 3. Valida

```bash
toolkit validate all --config candidates/{slug}/dataset.yml
```

### 4. Push GCS + BQ

```bash
cd ../dataset-incubator
python scripts/push_archive.py --layer clean --slug {slug} --create-bq-table --update-catalog --status clean_ready --dry-run
```

Se dry-run ok:

```bash
python scripts/push_archive.py --layer clean --slug {slug} --create-bq-table --update-catalog --status clean_ready
```

Include: parquet per ogni anno + `pipeline_run.json` + BQ external table `dataciviclab.{slug}.clean`.

### 5. Clean catalog

```bash
python scripts/build_clean_catalog.py --write
python scripts/build_clean_catalog.py --check-gcs
```

Aggiorna `clean_catalog.json` nella draft PR (`post-merge-candidate/pr-<N>-registry`):

- **sempre** — per compilare i campi mancanti: `name`, `description`, `source`, `columns[].role`, `columns[].description`
- **se slug nuovo** — crea l'entry completa
- **se `multi_file` flag cambiato** o **GCS path cambiato** — aggiorna struttura e path

```bash
# Checkout del branch della draft PR (creato dal workflow post-merge)
git fetch origin post-merge-candidate/pr-<N>-registry
git checkout post-merge-candidate/pr-<N>-registry

# Aggiungi le modifiche al catalog e pusha sul branch della PR
git add registry/clean_catalog.json
git commit -m "chore({slug}): aggiorna clean_catalog post-push GCS"
git push origin post-merge-candidate/pr-<N>-registry
```

### 6. Chiudi draft PR

`validate-clean-catalog.yml` gira automaticamente sulla PR quando il catalog cambia.
Verifica che passi, poi marca ready for review e fai merge.

## Stop rule

Se il run fallisce per fonte (timeout, schema cambiato) → apri issue, non procedere col push.

## Dove orientarsi

- [README.md](../README.md)
- [CONTRIBUTING.md](../CONTRIBUTING.md)
- [run-candidate.md](./run-candidate.md)
