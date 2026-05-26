---
name: run-candidate
description: Skill canonico di dataset-incubator per eseguire un candidate, verificare gli output e chiudere con uno stato tecnico chiaro.
license: MIT
metadata:
  version: "0.4"
  owner: "DataCivicLab"
  tags: [dataset-incubator, run, candidate, validation]
---

# Skill: run-candidate

Skill canonico di `dataset-incubator`.
Versione: 0.4 - 2026-05-06

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

Se il candidate è nuovo, manca `sql/clean.sql`, oppure lo scaffold non è ancora stato revisionato, non partire da `run all`.

Bootstrap:

```bash
toolkit run raw -c candidates/{slug}/dataset.yml -y 2024
```

Poi revisiona prima di proseguire:

- `sql/clean.sql` deve leggere da `raw_input`, non da `read_csv(...)`
- `clean.read` deve descrivere il parsing RAW quando serve
- eventuale proposta `clean.read`/profiling va incorporata nel `dataset.yml` solo dopo verifica

Run completo, quando `clean.sql` e mart SQL sono presenti e revisionati:

```bash
toolkit run full --config candidates/{slug}/dataset.yml --years 2024
```

`run full` esegue run all + validate + readiness in un comando, e processa automaticamente i support dichiarati in `dataset.yml` prima del candidate.

**`--years`**: specifica sempre l'anno. In CI viene rilevato automaticamente dalla matrice.

### 3. Verifica

La validazione è già inclusa in `run full`. Per eseguirla separatamente:

```bash
toolkit validate all --config candidates/{slug}/dataset.yml --years 2024
```

Oppure MCP: `toolkit_review_readiness(config_path)` → `ready | needs-review | incomplete`.

`validate all` controlla: esistenza parquet, coerenza run record/output, schema layer vs config.

### 4. Isola blocker se fallisce

In CI `blocker_count > 0` è gate hard — la PR fallisce.

In locale:

```bash
toolkit review-readiness --config candidates/{slug}/dataset.yml --year 2024 --json
```

Se il blocker è isolato → documenta e passa a stato `scaffolded_with_blocker`.

### 5. Diagnostica rapida (se serve)

```
toolkit_summary(config_path)         → tutti i layer a colpo d'occhio
toolkit_show_schema(config_path, layer="clean") → schema parquet prima di scrivere SQL
toolkit_raw_profile(config_path)      → encoding/delimiter dopo raw fallito
toolkit_list_runs(config_path, status="FAILED", limit=5) → pattern di fallimento
toolkit_run_summary(config_path)      → isolato o ricorrente?
toolkit_schema_diff(config_path)      → confronto schema raw cross-year (colonne, encoding)
```

**Quando usare `schema_diff`**:
- Dopo fallimento raw parsing — per vedere se encoding o colonne sono cambiate tra anni
- Prima di lanciare run su tutti gli anni — verifica consistenza schema source
- Durante review di candidate — segnala drift strutturale tra annualità

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
