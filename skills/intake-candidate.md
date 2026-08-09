---
name: intake-candidate
description: Skill canonico di dataset-incubator per portare un caso da issue intake a candidate runnable.
license: MIT
metadata:
  version: "0.7"
  owner: "DataCivicLab"
  tags: [dataset-incubator, intake, candidate]
---

# Skill: intake-candidate

Skill canonico di `dataset-incubator`.
Versione: 0.7 — 2026-07-31 — inspect come gate con readiness

## Obiettivo

Portare un caso da issue intake a candidate runnable — dataset.yml presente, run passa, stato tecnico chiaro.

## Entry point

- Issue con label `intake` e template `new-candidate.yml`, creata da un
  [source-check](https://github.com/dataciviclab/source-observatory/blob/main/skills/source-check.md)
  con verdetto `go intake`
- **Discussion Domanda** di riferimento: la domanda civica che ha motivato
  lo scouting, in `dataciviclab` categoria `Domanda`
- URL di una fonte pubblica già verificata (source-check non necessario se
  la fonte è già nota)

## Stop rule

Non proseguire se: source-check non completato con `go intake`, perimetro
instabile, `clean` è già mart, caso troppo esplorativo.

## Procedura

### 1. Valuta e allinea l'issue

Leggi: domanda guida, fonte, perimetro, output minimo, rischi noti, prossimo passo.

Se il candidate esiste già → riallinea l'issue al perimetro reale. Mai aprire un doppione.

Se il candidate non esiste, continua con la fase 2.

### 2. Preview e decisione (1-2 chiamate)

Scopo: capire se la fonte è utilizzabile prima di generare scaffold.

```bash
# Se è un portale CKAN:
toolkit_ckan_package_show(endpoint="https://portale.it", package_id="dataset-slug")
# → risorse, formato, DataStore, metadati

# Se è un file diretto CSV/TSV:
toolkit_preview_url("https://sito.it/dati.csv")
# → colonne, tipi, encoding, qualità

# Se non sai cos'è:
toolkit_probe_url_routed("https://sito.it/pagina")
# → routing automatico: CKAN | HTML | file
```

Se la fonte è ok → prosegui. Se è borderline → documenta il rischio nell'issue.

### 3. Bootstrap

```bash
cd candidates
toolkit scout https://sito.it/dati.csv --scaffold
cd ..
```

`toolkit scout --scaffold` (alias `-s`) genera: `dataset.yml`, `sql/clean.sql`,
`sql/mart.sql`, `README.md`, `notes.md`.

Se il candidate esiste già ma vuoi rigenerare lo scaffold:
```bash
toolkit run raw -c candidates/{slug}/dataset.yml -y 2024
```

> **Standard candidate**: ogni nuovo candidate deve rispettare
> [`docs/candidate-standard.md`](../docs/candidate-standard.md) — `source_id`,
> `tags`, `category`, `required_columns` + `not_null` sono obbligatori e
> verificati dal gate (`validate_candidate_structure.py`, strict).
> Verifica: `python scripts/validate_candidate_structure.py`.

### 4. Run

Prima di runnare, revisiona velocemente:
- `sql/clean.sql` — deve leggere da `raw_input`, niente parsing inline
- `clean.read` — parsing RAW esplicito quando serve (encoding, delimiter, skip)
- `dataset.yml` — campi `clean.read` e `sql` coerenti col source profile
- boundary clean/mart — clean raw-faithful, mart analitico

Poi, **un anno per volta**:

```bash
toolkit run -c candidates/{slug}/dataset.yml --year 2024
```

Esegue raw + clean + mart + validate + readiness. A fine run mostra il
verdict sintetico (es. `readiness: needs-review (7/8)`).

### 5. Verifica — inspect è il gate

Prima lascia che la pipeline dica se è tutto ok, poi controlla che i dati abbiano senso.

```bash
# 1. Stato + verdict readiness con check (comando unico)
toolkit inspect -c candidates/{slug}/dataset.yml -y 2024

# 2. Dati — conta righe e vedi un campione
toolkit inspect config -c candidates/{slug}/dataset.yml -l clean -m sql --sql "SELECT count(*) FROM data"
toolkit inspect config -c candidates/{slug}/dataset.yml -l clean -m preview --limit 5
# Oppure MCP: toolkit_layer(config_path, layer="clean", mode="preview", limit=5)

# 3. Se c'è mart, stessa verifica
toolkit inspect config -c candidates/{slug}/dataset.yml -l mart -m sql --sql "SELECT count(*) FROM data"
toolkit inspect config -c candidates/{slug}/dataset.yml -l mart -m preview --limit 5
```

I numeri sono nel range atteso? Le colonne sono quelle giuste?
Se `readiness: ready` → candidate ok.
Se `needs-review` → guarda quale check fallisce e decidi se è un blocker
reale o un check da allineare al perimetro.

Se la pipeline fallisce → diagnostica rapida:

```bash
# MCP
toolkit_layer(config_path, layer="raw", mode="profile")   → encoding/delimiter
toolkit_layer(config_path, layer="clean", mode="schema")  → schema parquet
toolkit_schema_diff(config_path)                          → drift colonne tra anni

# CLI
toolkit inspect config -c candidates/{slug}/dataset.yml -l raw -m profile --json
toolkit inspect config -c candidates/{slug}/dataset.yml -l clean -m schema --json
toolkit inspect config -c candidates/{slug}/dataset.yml --diff --json
```

Ciclo fix → run → inspect fino a `ready` (o blocker documentato).

Blocker specifico documentato, non formulaico.

### 6. PR

Apri PR con:
- branch da `main`
- perimetro stretto
- issue collegata
- esito del run + verdict readiness in descrizione (ready / needs-review motivato / blocker)

## Definition of done

- PR aperta con candidate strutturato
- issue e struttura coerenti
- almeno un run passato oppure blocker documentato
- boundary clean/mart rispettato

## Dove orientarsi

- [CONTRIBUTING.md](../CONTRIBUTING.md)
- [README.md](../README.md)
- [run-candidate.md](./run-candidate.md)
