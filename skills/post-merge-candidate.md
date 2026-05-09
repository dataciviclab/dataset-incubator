---
name: post-merge-candidate
description: Skill per il maintainer dopo il merge di un candidate in dataset-incubator. Run completo, push GCS, clean catalog.
license: MIT
metadata:
  version: "0.4"
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

### 4. Push GCS

**Trova lo slug GCS** (underscore, non trattino):
```bash
ls out/data/clean/          # per vedere lo slug corretto
```

**Dry run** (usa sempre il venv DI, non system python):
```bash
cd /path/to/dataset-incubator
.venv/bin/python scripts/push_archive.py --layer clean --slug {gcs_slug} --no-bq --update-catalog --status clean_ready --dry-run
```

Se dry-run ok, push reale senza BQ (BQ table creata separatamente dopo verifica):
```bash
.venv/bin/python scripts/push_archive.py --layer clean --slug {gcs_slug} --no-bq --update-catalog --status clean_ready
```

Parquet per ogni anno + `pipeline_run.json` → `gs://dataciviclab-clean/{gcs_slug}/{year}/`.

**BQ table — solo dopo verifica GCS ok:**
```bash
.venv/bin/python scripts/push_archive.py --layer clean --slug {gcs_slug} --create-bq-table --update-catalog --status clean_ready
```

### 5. Clean catalog — compila e normalizza

**Prima riscrivi** il catalog con `--write` per normalizzare, poi arricchisci i campi mancanti:

```bash
.venv/bin/python scripts/build_clean_catalog.py --write
```

**Compila entry per lo slug** (campi sempre da riempire):
- `name`: nome canonico, es. "MEF - Irpef Regionale"
- `description`: una frase che dice cosa contiene e da dove viene
- `source`: URL della fonte
- `columns[].role`: `dimension` o `metric`
- `columns[].description`: descrizione breve della colonna

Regole per `role`:
- colonne temporali, geografiche, categoriche → `dimension`
- colonne numeriche (freq, eur, count) → `metric`

**Verifica e push**:
```bash
.venv/bin/python scripts/build_clean_catalog.py --check-gcs   # deve tornare "ok"
git add registry/clean_catalog.json
git commit -m "chore(post-merge): aggiorna registry per PR #<N>"
git push origin post-merge-candidate/pr-<N>-registry
```

Aggiorna `clean_catalog.json` nella draft PR (`post-merge-candidate/pr-<N>-registry`):
- **sempre** — per compilare i campi mancanti
- **se slug nuovo** — crea l'entry completa
- **se `multi_file` flag cambiato** o **GCS path cambiato** — aggiorna struttura e path

### 6. Chiudi draft PR

Verifica che `--check-gcs` sia green, poi marca la PR ready for review e fai merge.

## Stop rule

Se il run fallisce per fonte (timeout, schema cambiato) → apri issue, non procedere col push.

## Dove orientarsi

- [README.md](../README.md)
- [CONTRIBUTING.md](../CONTRIBUTING.md)
- [run-candidate.md](./run-candidate.md)
