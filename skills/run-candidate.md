---
name: run-candidate
description: Skill canonico per eseguire un candidate esistente e verificarlo end-to-end con readiness come gate.
license: MIT
metadata:
  version: "0.7"
  owner: "DataCivicLab"
  tags: [dataset-incubator, run, candidate]
---

# Skill: run-candidate

Skill canonico di `dataset-incubator`.
Versione: 0.7 — 2026-07-31 — flusso end-to-end con readiness come gate

## Obiettivo

Eseguire un candidate già presente in `candidates/` e chiudere con stato:
`runnable` | `scaffolded_with_blocker`.

## Entry point

- `candidates/{slug}/dataset.yml` esistente
- Toolkit accessibile (v1.47+)

Stop: candidate immaturo, boundary clean/mart assente, problema di fase precedente.

## Regole

1. **Mai guardare solo l'exit code** — `run` può passare con warning. `inspect` mostra i check.
2. **Un anno per volta** durante lo sviluppo, non tutti gli anni configurati.
3. **`inspect` è il gate** — il run ti dice "è andato", `inspect` ti dice "è buono".
4. **Blocker > formula** — se qualcosa fallisce, documenta il *perché* preciso, non "non funziona".

## Procedura

### 1. Pre-flight — capire dove siamo

```bash
toolkit inspect -c candidates/{slug}/dataset.yml -y 2024
```

Il comando unico mostra: run status, righe/colonne per layer, raw hints e
**verdict readiness con check**. Risponde a: il dataset è mai stato runnato?
è pronto? cosa manca?

Oppure MCP: `toolkit_status(config_path)` → sezione readiness.

### 2. Run — un anno per volta

```bash
toolkit run -c candidates/{slug}/dataset.yml --year 2024
```

Esegue raw + clean + mart + validazione + readiness. A fine run mostra il
verdict sintetico: `readiness: needs-review (7/8)`.

### 3. Verifica — inspect è il gate

```bash
# Stato + verdict + check (comando unico)
toolkit inspect -c candidates/{slug}/dataset.yml -y 2024

# Ispezione dati — conta righe e campione
toolkit inspect config -c candidates/{slug}/dataset.yml -l clean -m sql --sql "SELECT count(*) FROM data"
toolkit inspect config -c candidates/{slug}/dataset.yml -l clean -m preview --limit 5
# Oppure MCP: toolkit_layer(config_path, layer="clean", mode="preview", limit=5)

# Se c'è mart
toolkit inspect config -c candidates/{slug}/dataset.yml -l mart -m sql --sql "SELECT count(*) FROM data"
toolkit inspect config -c candidates/{slug}/dataset.yml -l mart -m preview --limit 5
```

Se `readiness: ready` → chiudi con `runnable`.
Se `needs-review` → guarda **quale check fallisce** nell'output di inspect
(es. `validation_rules_coverage`) e decidi: è un blocker reale o un check
da allineare al perimetro del dataset?

### 4. Diagnostica (se fallisce o il verdict non torna)

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

### 5. Ciclo fino a ready

fix → run → inspect → fix → run → inspect.
Fermati quando `readiness: ready`, oppure `needs-review` con blocker
documentato con precisione.

### 6. Chiudi con stato

- `runnable` — run passa, `readiness: ready` o `needs-review` motivato
- `scaffolded_with_blocker` — blocker preciso documentato

## Definition of done

- run eseguito, inspect conferma il verdict
- esito netto (ready / blocker documentato), prossimo passo esplicito

## Errori tipici

- lanciare tutti gli anni invece di un anno singolo
- guardare solo exit code, non il verdict readiness né gli output reali
- cambiare troppe cose dopo il primo errore
- chiudere `runnable` con check falliti non motivati

## Dove orientarsi

- [README.md](../README.md)
- [intake-candidate.md](./intake-candidate.md)
