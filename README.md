# dataset-incubator — Il laboratorio tecnico dei dati del Lab

**Qui nascono i dataset. Dalla prima idea alla pipeline pubblica, passo per passo.**

Ogni dataset del DataCivicLab nasce qui: si valida la fonte, si testa la pipeline,
si stabilizza l'output minimo. Quando è pronto, esce verso il suo repo definitivo.

## Flusso

```
source-observatory  →  dataset-incubator  →  toolkit  →  GCS  →  data-explorer
```

| Fase | Cosa succede |
|---|---|
| **Intake** | Issue con label `intake` — si valuta se il caso è maturo |
| **Candidate** | `candidates/<slug>/` con dataset.yml, SQL, notes.md |
| **Run** | Post-merge: toolkit esegue raw → clean → mart, aggiorna registry |
| **Uscita** | Verso repo dedicato (open-pnrr, open-siope...) o `dataciviclab/analisi/` |

## Struttura

```text
candidates/           filoni attivi e passati
support_datasets/     basi trasversali riusabili (anagrafiche, dizionari)
registry/             artifact registry (ADR-001)
templates/            template per nuovi candidate
skills/               workflow markdown per umani e agenti
scripts/              build, validazione, push artifact
tests/                test per script e validazione
```

## Candidati attivi

Vedi le [issue con label `incubating`](https://github.com/dataciviclab/dataset-incubator/issues?q=is%3Aopen+label%3Aincubating) per i filoni in lavorazione.

## Come contribuire

- [CONTRIBUTING.md](CONTRIBUTING.md) — regole per issue, PR e struttura candidate
- [skills/intake-candidate.md](skills/intake-candidate.md) — workflow per valutare un nuovo candidato
- [skills/run-candidate.md](skills/run-candidate.md) — esecuzione manuale end-to-end
