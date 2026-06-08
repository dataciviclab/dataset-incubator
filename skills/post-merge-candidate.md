---
name: post-merge-candidate
description: Skill per il maintainer dopo il merge di un candidate in dataset-incubator.
license: MIT
metadata:
  version: "0.5"
  owner: "DataCivicLab"
  tags: [dataset-incubator, candidate, gcs, push, maintainer]
---

# Skill: post-merge-candidate

Skill per il maintainer dopo il merge di una PR candidate in `dataset-incubator`.

## Obiettivo

Validare e chiudere la draft PR `chore(post-merge): aggiorna registry per PR #<num>` aperta dal workflow CI.

## Entry point

- PR mergiata su `candidates/` o `support_datasets/`
- Draft PR `chore(post-merge): aggiorna registry per PR #<num>` già aperta da CI

## Cosa fa già CI (GHA `Post-Merge Candidate Registry`)

- ✅ toolkit run full (tutti gli anni)
- ✅ push clean parquet su GCS
- ✅ `registry/pipeline_signals.json` aggiornato
- ✅ `registry/clean_catalog.json` auto-derivato
- ✅ draft PR aperta

## Cosa rimane al maintainer

### 1. Compila i campi del clean catalog

Solo per slug nuovi. Apri `registry/clean_catalog.json` e compila:

| Campo | Cosa mettere |
|---|---|
| `name` | Nome canonico, es. "PIL regionale e provinciale" |
| `description` | Una frase: cosa contiene, da dove viene |
| `source` | Nome ente o URL breve |
| `source_id` | ID fonte da source-observatory (es. `istat_sdmx`) |
| `columns[].role` | `dimension` per geo/tempo/categoria, `metric` per numeri |
| `columns[].description` | Descrizione breve della colonna |

Regole per `role`:
- temporale, geografica, categorica → `dimension`
- numerica (freq, eur, count) → `metric`

### 2. Verifica

```bash
python scripts/build_clean_catalog.py --check-gcs
```

Deve restituire `ok`.

### 3. Chiudi

```bash
git add registry/clean_catalog.json
git commit -m "fix: compila entry {slug} nel clean catalog"
git push origin post-merge-candidate/pr-<N>-registry
```

Marca la PR ready for review e mergia.

## Stop rule

Se il run CI è fallito (fonte irraggiungibile, timeout), non procedere. Usa gli artifact `sample-run-*` per diagnosticare, poi apri issue.

## Dove orientarsi

- [README.md](../README.md)
- [CONTRIBUTING.md](../CONTRIBUTING.md)
- [run-candidate.md](./run-candidate.md)
