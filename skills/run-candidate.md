---
name: run-candidate
description: Skill canonico di dataset-incubator per eseguire un candidate, verificare gli output e chiudere con uno stato tecnico chiaro.
license: MIT
metadata:
  version: "0.3"
  owner: "DataCivicLab"
  tags: [dataset-incubator, run, candidate, validation]
---

# Skill: run-candidate

Skill canonico di `dataset-incubator`.
Versione: 0.3 - 2026-05-03

## Obiettivo

Eseguire un candidate esistente e chiudere con stato: `runnable` | `scaffolded_with_blocker` | `wait`.

## Entry point

- Candidate con struttura minima (`dataset.yml`, `sql/`, `README.md` o `notes.md`)
- Config entrypoint chiaro
- Accesso a `toolkit/`

Stop: candidate immaturo, boundary clean/mart assente, problema di fase precedente.

## Procedura

### 1. Pre-flight

```bash
toolkit inspect paths --config candidates/{slug}/dataset.yml --json
```

Oppure MCP: `toolkit_inspect_paths(config_path)` → `run_file_count >= 1`, `latest_run.status` verificato.

### 2. Run

```bash
toolkit run all --config candidates/{slug}/dataset.yml --years 2024
```

**Two-phase**: se `dataset.yml` ha `support`, i support girano prima del main — in locale e in CI.

**`--years`**: specifica sempre l'anno. In CI viene rilevato automaticamente dalla matrice.

### 3. Valida

```bash
toolkit validate all --config candidates/{slug}/dataset.yml --years 2024
```

Oppure MCP: `toolkit_review_readiness(config_path)` → `ready | needs-review | incomplete`.

`validate all` controlla: esistenza parquet, coerenza run record/output, schema layer vs config.

### 4. Isola blocker se fallisce

In CI `blocker_count > 0` è gate hard — la PR fallisce.

In locale:

```bash
toolkit blocker-hints --config candidates/{slug}/dataset.yml --year 2024 --json
```

Se il blocker è isolato → documenta e passa a stato `scaffolded_with_blocker`.

### 5. Diagnostica rapida (se serve)

```
toolkit_summary(config_path)         → tutti i layer a colpo d'occhio
toolkit_show_schema(config_path, layer="clean") → schema parquet prima di scrivere SQL
toolkit_raw_profile(config_path)      → encoding/delimiter dopo raw fallito
toolkit_list_runs(config_path, status="FAILED", limit=5) → pattern di fallimento
toolkit_run_summary(config_path)      → isolato o ricorrente?
```

### 6. Chiudi con stato

- `runnable` — run passa, output leggibili
- `scaffolded_with_blocker` — blocker preciso documentato
- `wait` — manca un pezzo di fase precedente

## Definition of done

- entrypoint chiaro
- esito netto
- output verificato oppure blocker preciso
- prossimo passo esplicito

## Errori tipici

- partire dal config sbagliato
- lanciare compose prima dei source layer
- guardare solo exit code, non gli output reali
- cambiare troppe cose dopo il primo errore

## Dove orientarsi

- [README.md](../README.md)
- [CONTRIBUTING.md](../CONTRIBUTING.md)
- [intake-candidate.md](./intake-candidate.md)
