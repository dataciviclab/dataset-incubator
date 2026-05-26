---
name: intake-candidate
description: Skill canonico di dataset-incubator per portare un caso da issue intake a PR pronta per merge.
license: MIT
metadata:
  version: "0.5"
  owner: "DataCivicLab"
  tags: [dataset-incubator, intake, candidate, support-dataset]
---

# Skill: intake-candidate

Skill canonico di `dataset-incubator`.
Versione: 0.5 - 2026-05-09

## Obiettivo

Portare un caso da issue intake a PR mergiata — candidate strutturato, runnable, pronto per il post-merge.

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

### 2. Bootstrap

Due modalità secondo il punto di partenza:

**Source nuova, hai un URL diretto al file:**

```bash
cd candidates
toolkit scout https://example.com/data.csv --scaffold
cd ..
```

`toolkit scout --scaffold` (alias `-s`) genera: `dataset.yml`, `sql/clean.sql`,
`sql/mart.sql`, `README.md`, `notes.md`, `notebooks/`. Lo scaffold è creato in
`./{slug}/` — esegui il comando da dentro `candidates/` per avere il candidate
nella posizione giusta.

Se vuoi anche eseguire subito il run raw dopo lo scaffold, aggiungi `--run` (alias `-r`).

**Candidate strutturato già esistente, vuoi rigenerare lo scaffold:**
```bash
toolkit run raw -c candidates/{slug}/dataset.yml -y 2024
```

### 3. Struttura

Completa quello che `toolkit scout --scaffold` ha lasciato vuoto. Template in `templates/candidate/`:
- `README.md` — descrivi il candidate
- `notes.md` — domanda guida, rischi, note operative
- `notebooks/<slug>_v0.ipynb` — copia dal template, imposta `METRICA` / `METRICA_CLEAN` nella cella setup

Se il candidate usa `support`, verifica che sia necessario e non sostituibile con un join a mart esistente.

### 4. Revisiona scaffold

Prima di lanciare il run, revisiona:

- `sql/clean.sql` — deve leggere da `raw_input`, niente parsing inline
- `clean.read` — parsing RAW esplicito quando serve (encoding, delimiter, skip rows)
- `dataset.yml` — campi `clean.read` e `clean.sql` coerenti col source profile
- boundary clean/mart — clean raw-faithful, mart analitico

### 5. Run e valida

Vedi [run-candidate.md](./run-candidate.md) per procedura completa.

```bash
toolkit run full --config candidates/{slug}/dataset.yml --years 2024
```

Usa `--strict-config` per intercettare campi legacy o deprecati.

Se fallisce → `toolkit_review_readiness(config_path)` per isolare il primo errore. Blocker specifico documentato, non formulaico.

### 6. PR

Apri PR con:
- branch da `main`
- perimetro stretto
- issue collegata
- esito del run in descrizione (passed / failed / blocker)

## Definition of done

- PR aperta con candidate strutturato
- issue e struttura coerenti
- almeno un run verificato oppure blocker documentato
- boundary clean/mart rispettato

## Dove orientarsi

- [CONTRIBUTING.md](../CONTRIBUTING.md)
- [README.md](../README.md)
- [run-candidate.md](./run-candidate.md)