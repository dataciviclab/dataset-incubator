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

Pattern snello (eurostat post-merge-registry.yml):
- ✅ run completo dei dataset cambiati (parquet locali) + push GCS
- ✅ `python scripts/build_registry.py --write` (wrapper su `toolkit.registry`):
  - `registry/registry.json` — artifact unico (fusion ADR, toolkit v1.49.0):
    sezioni datasets/marts/signals/codelists/entities; metadata dal dataset.yml,
    schema dai parquet appena runnati; entry non cambiate preservate dal
    catalogo esistente
  - proiezioni legacy per i consumer non ancora migrati (clean_query_mcp,
    data-explorer, agent-context-builder): `registry/clean_catalog.json`,
    `registry/pipeline_signals.json`, `registry/entity_graph.json`
- ✅ draft PR aperta

## Cosa rimane al maintainer

I campi del catalogo (name/description/source/tags/category) arrivano dal
`dataset.yml`; le entry già presenti restano dal catalogo esistente. Il
maintainer interviene **solo per i casi editoriali rari**: descrizioni umane
di qualità per slug nuovi (il `name` derivato `slug.title()` non è un buon
titolo). In quel caso compila direttamente in `registry/registry.json`
(sezione `datasets`) della PR draft:

### 1. (Raro) Compila i campi editoriali del registry

Solo per slug nuovi con titolo/descrizione derivati poco leggibili. Apri
`registry/registry.json` (sezione `datasets`) e compila:

| Campo | Cosa mettere |
|---|---|
| `name` | Nome canonico, es. "PIL regionale e provinciale" |
| `description` | Una frase: cosa contiene, da dove viene |
| `source` | Nome ente o URL breve |
| `columns[].role` | `dimension` per geo/tempo/categoria, `metric` per numeri |
| `columns[].description` | Descrizione breve della colonna |

Regole per `role`:
- temporale, geografica, categorica → `dimension`
- numerica (freq, eur, count) → `metric`

### 2. Verifica

```bash
python scripts/build_registry.py --check-gcs
```

Deve restituire `ok`.

### 3. Chiudi

```bash
git add registry/
git commit -m "fix: compila entry {slug} nel registry"
git push origin post-merge-candidate/pr-<N>-registry
```

Marca la PR ready for review e mergia.

## Stop rule

Se il run CI è fallito (fonte irraggiungibile, timeout), non procedere. Usa gli artifact `sample-run-*` per diagnosticare, poi apri issue.

## Dove orientarsi

- [README.md](../README.md)
- [CONTRIBUTING.md](../CONTRIBUTING.md)
- [run-candidate.md](./run-candidate.md)
