---
name: post-merge-candidate
description: Checklist per il maintainer dopo il merge di un candidate/support dataset in dataset-incubator. Produce clean parquet in GCS e completa il registry draft PR.
license: MIT
metadata:
  version: "0.2"
  owner: "DataCivicLab"
  tags: [dataset-incubator, candidate, gcs, push]
---

# Workflow: post-merge-candidate

Workflow da seguire dopo il merge di una PR candidate/support dataset in `dataset-incubator`.
Richiede accesso in scrittura a GCS (`dataciviclab-clean`).

Il workflow GitHub `Post-Merge Candidate Registry` apre una draft PR di handoff
quando viene mergiata una PR che modifica `candidates/**` o `support_datasets/**`.
La draft PR aggiorna automaticamente `registry/pipeline_signals.json`, esegue un
sample-run CI sui config path modificati, salva l'esito in `sample_run` dentro il
signal corrispondente e contiene la checklist per completare run, push GCS/BQ e
aggiornamento del clean catalog.
Se la rigenerazione di `pipeline_signals.json` non produce differenze, il workflow
apre comunque la draft PR con un commit vuoto di handoff.

## Quando eseguire

Dopo il merge di una PR che aggiunge o aggiorna:

- un candidate in `candidates/{slug}/`
- un support dataset in `support_datasets/{slug}/`

## Step

### 1. Apri la draft PR post-merge

Controlla la draft PR aperta dal workflow `Post-Merge Candidate Registry`.
Quella PR sostituisce la vecchia follow-up issue e resta draft finché il push
GCS/BQ e il catalog sono verificati.

La PR riporta l'esito del sample-run CI, linka gli artifact `sample-run-*` e
aggiorna il campo `sample_run` nel relativo signal di `pipeline_signals.json`.
Se il sample-run fallisce, usa gli artifact per diagnosticare prima di procedere
con il run completo.

### 2. Aggiorna il repo locale

```bash
git pull origin main
```

### 3. Runna il candidato con toolkit

```bash
cd dataset-incubator
toolkit run all --config candidates/{slug}/dataset.yml
# oppure per multi-source:
toolkit run all --config candidates/{slug}/sources/{source}/dataset.yml
# oppure per support dataset:
toolkit run all --config support_datasets/{slug}/dataset.yml
```

Verifica che il run completi senza errori e che `out/data/clean/{slug}/` sia popolato.

### 4. Validazione (opzionale ma raccomandata)

```bash
toolkit validate all --config candidates/{slug}/dataset.yml
```

### 5. Push clean su GCS + BQ

```bash
python scripts/push_archive.py --layer clean --slug {slug} --create-bq-table --update-catalog --status clean_ready --dry-run
```

Se il dry-run è ok, esegui per davvero:

```bash
python scripts/push_archive.py --layer clean --slug {slug} --create-bq-table --update-catalog --status clean_ready
```

Il push include:
- parquet clean per ogni anno
- `pipeline_run.json` (traccia del run) accanto ad ogni anno
- external table BQ `dataciviclab.{slug}.clean` che punta ai file GCS

### 6. Aggiorna catalog **solo dopo push GCS**

```bash
# Normalizza il catalog dopo l'eventuale update fatto da push_archive.py
python scripts/build_clean_catalog.py --write

# Verifica che i path pubblici siano risolvibili
python scripts/build_clean_catalog.py --check-gcs
```

**Regola**: aggiorna `registry/clean_catalog.json` nella draft PR solo se:
- è uno **slug nuovo** (non esiste ancora in `registry/clean_catalog.json`)
- oppure è cambiato il `multi_file` flag (da `false` a `true` o viceversa)
- oppure il GCS path è cambiato (es.vecchio `2024/file.parquet` → nuovo `*/file_*.parquet`)

**Non aggiornare** se:
- `multi_file: false` e lo slug già esiste con path corretto (il catalog è già allineato)
- solo il contenuto del parquet è cambiato (stesso path GCS, stesse colonne)

Se serve aggiornare:

```bash
git add registry/clean_catalog.json
git commit -m "chore({slug}): aggiorna clean_catalog post-push GCS"
git push
```

### 7. Verifica

Il workflow `validate-clean-catalog` parte automaticamente sulla draft PR quando
`registry/clean_catalog.json` cambia. Controlla che passi, poi marca la PR ready
for review.

## Note

- Il mart non viene pushato in questo step — va fatto on-demand dopo analisi.
- Se il run fallisce per problemi di fonte (timeout, schema cambiato), apri issue nel repo prima di procedere.
- Il `pipeline_signals.json` si aggiorna automaticamente nella draft PR post-merge.
- Se `pipeline_signals.json` resta invariato, la draft PR viene comunque aperta come contenitore operativo.
- Il sample-run CI è una verifica rapida: non sostituisce il run completo del maintainer e non pubblica nulla.
- Il campo `sample_run` registra solo l'esito CI del sample-run; la pubblicazione GCS resta tracciata dal clean catalog.
- `clean_catalog.json` va completato solo dopo il push GCS/BQ: prima del push non può dichiarare path pubblici affidabili.
- `--update-catalog` nel `push_archive.py` esegue un upsert del catalog — usalo insieme a `build_clean_catalog.py --write` e `--check-gcs`.
