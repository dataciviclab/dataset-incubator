# Skills — dataset-incubator

Skill procedurali per agenti AI e operatori tecnici di `dataset-incubator`.

Sono il riferimento umano per il comportamento della pipeline toolkit e delle GitHub Actions. Le Actions in `.github/workflows/` sono l'esecuzione automatica — questi skill ne spiegano il flusso.

## Skill disponibili

| Skill | Quando |
|---|---|
| `intake-candidate.md` | Valutare se un caso è maturo per entrare in DI e creare la struttura minima |
| `run-candidate.md` | Eseguire un candidate e chiuderlo con stato (`runnable`, `scaffolded_with_blocker`, `wait`) |
| `post-merge-candidate.md` | Checklist maintainer dopo il merge: run completo, push GCS, clean catalog |

## GitHub Actions (pipeline automatica)

| Action | Trigger | Cosa fa |
|---|---|---|---|
| `validate-candidate-structure.yml` | PR su candidates/, support_datasets/ | Verifica che ogni candidate abbia `dataset.yml` e struttura valida |
| `lint.yml` | PR e push su scripts/, tools/, pyproject.toml | Mypy + ruff + pytest su codice Python |
| `pr-toolkit-check.yml` | PR su candidates/, support_datasets/ | `toolkit run all` + `validate all` + gate blocker_hints + artifact `sample-run-*` |
| `post-merge-candidate.yml` | Merge su candidates/, support_datasets/ | Consuma artifact del PR check, aggiorna `pipeline_signals.json`, apre draft PR handoff |
| `build-pipeline-signals.yml` | Manuale (workflow_dispatch) | Ricostruisce `registry/pipeline_signals.json` |
| `validate-clean-catalog.yml` | PR e push su `registry/` | Schema JSON, GCS check, clean-query smoke test |

## Cross-repo

| Risorsa | Dove | Quando |
|---|---|---|
| `promote-analisi` | `lab-ops/skills/` | Quando un filone è pronto per `dataciviclab/analisi/` |

## Struttura

```
dataset-incubator/
  skills/                   # skill markdown (riferimento umano)
    intake-candidate.md
    run-candidate.md
    post-merge-candidate.md
    README.md
  .github/workflows/        # GitHub Actions (esecuzione automatica)
```
