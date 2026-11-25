# Skills — dataset-incubator

Skill procedurali per agenti AI e operatori tecnici di `dataset-incubator`.

Sono il riferimento umano per il comportamento della pipeline toolkit e delle GitHub Actions. Le Actions in `.github/workflows/` sono l'esecuzione automatica — questi skill ne spiegano il flusso.

## Skill disponibili

| Skill | Quando |
|---|---|
| `intake-candidate.md` | Valutare se un caso è maturo per entrare in DI e creare la struttura minima |
| `run-candidate.md` | Eseguire un candidate e chiuderlo con stato (`runnable`, `scaffolded_with_blocker`, `wait`) — inspect come gate |
| `post-merge-candidate.md` | Checklist maintainer dopo il merge: run completo, push GCS, clean catalog |

> **Gate**: dopo ogni run, `toolkit inspect` mostra il verdict readiness (ready / needs-review / incomplete) con i check. Un candidate si chiude `runnable` solo con `ready` o con `needs-review` motivato per il perimetro del dataset.

## GitHub Actions (pipeline automatica)

| Action | Trigger | Cosa fa |
|---|---|---|---|
| `check.yml` | PR e push su main | Lint + mypy + pytest (`python-ci`) e preflight dei dataset cambiati (`dataset-config-check-reusable`) |
| `pipeline.yml` | Merge su candidates/, compose/, support_datasets/ + dispatch | `pipeline-reusable`: detect, run, sync GCS, registry PR |
| `smoke-weekly.yml` | Schedule settimanale | Probe raggiungibilità fonti + verifica `registry.json` |

## Cross-repo

| Risorsa | Dove | Quando |
|---|---|---|
| `new-analysis` | `dataciviclab/skills/` | Quando un filone è pronto per `dataciviclab/analisi/` |

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
