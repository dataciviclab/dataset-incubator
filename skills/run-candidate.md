---
name: run-candidate
description: Skill canonico per eseguire un candidate esistente e verificarne lo stato.
license: MIT
metadata:
  version: "0.5"
  owner: "DataCivicLab"
  tags: [dataset-incubator, run, candidate]
---

# Skill: run-candidate

Skill canonico di `dataset-incubator`.
Versione: 0.5 - 2026-06-17

## Obiettivo

Eseguire un candidate già presente in `candidates/` e chiudere con stato:
`runnable` | `scaffolded_with_blocker`.

## Entry point

- `candidates/{slug}/dataset.yml` esistente
- Toolkit accessibile

Stop: candidate immaturo, boundary clean/mart assente, problema di fase precedente.

## Procedura

### 1. Pre-flight

```bash
toolkit inspect summary -c candidates/{slug}/dataset.yml -y 2024 --json
```

Oppure MCP: `toolkit_status(config_path)` → sezioni `paths_info` + `run_stats`.

### 2. Run

```bash
toolkit run full --config candidates/{slug}/dataset.yml --years 2024
```

Unico comando. Esegue raw + clean + mart + validate + readiness in sequenza.

### 3. Verifica

Prima lo stato pipeline, poi controlla che i dati abbiano senso.

```bash
# Stato pipeline
toolkit inspect summary -c candidates/{slug}/dataset.yml -y 2024 --json
# Oppure MCP: toolkit_status(config_path) → sezione readiness

# Ispezione dati — conta righe e campione
toolkit inspect config -c candidates/{slug}/dataset.yml -l clean -m sql --sql "SELECT count(*) FROM data"
toolkit inspect config -c candidates/{slug}/dataset.yml -l clean -m preview --limit 5
# Oppure MCP: toolkit_layer(config_path, layer="clean", mode="preview", limit=5)

# Se c'è mart
toolkit inspect config -c candidates/{slug}/dataset.yml -l mart -m sql --sql "SELECT count(*) FROM data"
toolkit inspect config -c candidates/{slug}/dataset.yml -l mart -m preview --limit 5
```

### 4. Diagnostica (se fallisce)

```bash
# MCP (raccomandato)
toolkit_layer(config_path, layer="raw", mode="profile")   → encoding/delimiter
toolkit_layer(config_path, layer="clean", mode="schema")  → schema parquet
toolkit_schema_diff(config_path)                           → drift colonne tra anni
toolkit_list_runs(config_path, status="FAILED", limit=5)  → pattern di fallimento

# CLI equivalente
toolkit inspect config -c candidates/{slug}/dataset.yml -l raw -m profile --json
toolkit inspect config -c candidates/{slug}/dataset.yml -l clean -m schema --json
toolkit inspect config -c candidates/{slug}/dataset.yml --diff --json
```

Se il blocker è isolato → documentalo e chiudi con `scaffolded_with_blocker`.

### 5. Chiudi con stato

- `runnable` — run full passa, output leggibili
- `scaffolded_with_blocker` — blocker preciso documentato

## Definition of done

- run full eseguito senza errori oppure blocker documentato
- esito netto, prossimo passo esplicito

## Errori tipici

- lanciare compose prima dei source layer
- guardare solo exit code, non gli output reali
- cambiare troppe cose dopo il primo errore

## Dove orientarsi

- [README.md](../README.md)
- [intake-candidate.md](./intake-candidate.md)
