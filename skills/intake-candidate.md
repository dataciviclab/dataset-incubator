---
name: intake-candidate
description: Skill canonico di dataset-incubator per portare un caso da issue intake a candidate runnable.
license: MIT
metadata:
  version: "0.6"
  owner: "DataCivicLab"
  tags: [dataset-incubator, intake, candidate]
---

# Skill: intake-candidate

Skill canonico di `dataset-incubator`.
Versione: 0.6 - 2026-06-17

## Obiettivo

Portare un caso da issue intake a candidate runnable — dataset.yml presente, run full passa, stato tecnico chiaro.

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
`sql/mart.sql`, `README.md`, `notes.md`, `notebooks/`.

Se il candidate esiste già ma vuoi rigenerare lo scaffold:
```bash
toolkit run raw -c candidates/{slug}/dataset.yml -y 2024
```

### 4. Run

Prima di runnare, revisiona velocemente:
- `sql/clean.sql` — deve leggere da `raw_input`, niente parsing inline
- `clean.read` — parsing RAW esplicito quando serve (encoding, delimiter, skip)
- `dataset.yml` — campi `clean.read` e `sql` coerenti col source profile
- boundary clean/mart — clean raw-faithful, mart analitico

Poi:

```bash
toolkit run full --config candidates/{slug}/dataset.yml --years 2024
```

Unico comando. Esegue raw + clean + mart + validate + readiness.

### 5. Verifica

Prima lascia che la pipeline dica se è tutto ok, poi controlla che i dati abbiano senso.

```bash
# 1. Stato pipeline
toolkit inspect summary -c candidates/{slug}/dataset.yml -y 2024 --json
# Oppure MCP: toolkit_status(config_path) → paths, summary, readiness, run_stats

# 2. Dati — conta righe e vedi un campione
toolkit inspect config -c candidates/{slug}/dataset.yml -l clean -m sql --sql "SELECT count(*) FROM data"
toolkit inspect config -c candidates/{slug}/dataset.yml -l clean -m preview --limit 5
# Oppure MCP: toolkit_layer(config_path, layer="clean", mode="preview", limit=5)

# 3. Se c'è mart, stessa verifica
toolkit inspect config -c candidates/{slug}/dataset.yml -l mart -m sql --sql "SELECT count(*) FROM data"
toolkit inspect config -c candidates/{slug}/dataset.yml -l mart -m preview --limit 5
```

I numeri sono nel range atteso? Le colonne sono quelle giuste? Se sì → candidate ok.

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

Blocker specifico documentato, non formulaico.

### 6. PR

Apri PR con:
- branch da `main`
- perimetro stretto
- issue collegata
- esito del run in descrizione (passed / failed / blocker)

## Definition of done

- PR aperta con candidate strutturato
- issue e struttura coerenti
- almeno un run full passato oppure blocker documentato
- boundary clean/mart rispettato

## Dove orientarsi

- [CONTRIBUTING.md](../CONTRIBUTING.md)
- [README.md](../README.md)
- [run-candidate.md](./run-candidate.md)
