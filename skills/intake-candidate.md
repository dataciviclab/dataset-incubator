---
name: intake-candidate
description: Skill canonico di dataset-incubator per portare un caso da issue intake a PR pronta per merge.
license: MIT
metadata:
  version: "0.3"
  owner: "DataCivicLab"
  tags: [dataset-incubator, intake, candidate, support-dataset]
---

# Skill: intake-candidate

Skill canonico di `dataset-incubator`.
Versione: 0.3 - 2026-05-03

## Obiettivo

Portare un caso da issue intake a PR mergiata — candidate strutturato, runnable, pronto per il post-merge.

## Entry point

- Issue con label `intake` e template `new-candidate.yml`
- Creata automaticamente da `discussion-to-intake.yml` (in `dataciviclab`) oppure aperta direttamente

## Stop rule

Non proseguire se: source-check debole, `clean` è già mart, caso troppo esplorativo, perimetro instabile.

## Procedura

### 1. Valuta e allinea l'issue

Legate: domanda guida, fonte, perimetro, output minimo, rischi noti, prossimo passo.

Se il candidate esiste già → riallinea l'issue al perimetro reale. Mai aprire un doppione.

### 2. Crea la struttura

Single-source:

```
candidates/<slug>/
  dataset.yml
  README.md
  notes.md
  notebooks/<slug>_v0.ipynb
  sql/clean.sql, mart.sql
```

Copia il notebook da `templates/candidate/notebooks/` e imposta `METRICA` / `METRICA_CLEAN` in cima alla cella setup.

### 3. Two-phase se c'è support

Se `dataset.yml` dichiara `support`, i support girano prima del main.

Verifica che siano necessari e non sostituibili con un join a mart esistente.

### 4. Run e valida

Check rapido pre-flight:

```bash
toolkit inspect paths --config candidates/{slug}/dataset.yml --json
```

Oppure MCP: `toolkit_inspect_paths(config_path)` → path contract verificato.

Run + valida:

```bash
toolkit run all --config candidates/{slug}/dataset.yml --years 2024
toolkit validate all --config candidates/{slug}/dataset.yml --years 2024
```

Usa `--strict-config` per intercettare campi legacy o deprecati:

```bash
toolkit run all --config candidates/{slug}/dataset.yml --years 2024 --strict-config
```

Se fallisce → MCP `toolkit_blocker_hints(config_path)` per isolare il primo errore. Blocker specifico documentato, non formulaico.

### 5. PR

Apri PR con:

- branch da `main`
- perimetro stretto
- issue collegata
- esito del run in descrizione (passed / failed / blocker)

### 6. Chiudi l'issue

Passa label: `intake` → `incubating`.

Stato candidato: `runnable` se il run passa, `scaffolded_with_blocker` se c'è blocker, `wait` se non è il momento.

## Definition of done

- PR aperta con candidate strutturato
- issue e struttura coerenti
- almeno un run verificato oppure blocker documentato
- notebook v0 reale
- boundary clean/mart rispettato

## Dove orientarsi

- [CONTRIBUTING.md](../CONTRIBUTING.md)
- [README.md](../README.md)
- [run-candidate.md](./run-candidate.md)
