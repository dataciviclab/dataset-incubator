# dataset-incubator

Repo di incubazione tecnica per i dataset candidati e le basi trasversali del Lab.

Qui si valida la fonte, si restringe la domanda e si stabilizza l'output minimo.

Un **filone** è un percorso di lavoro che parte da una domanda civica e arriva a un dataset o un'analisi pubblica. Il contratto tecnico di ogni filone (`dataset.yml`, SQL, pipeline) vive qui in modo permanente — anche quando il lavoro pubblico finisce altrove.

## Come funziona il flusso

```
source-observatory  →  dataset-incubator  →  toolkit  →  GCS  →  data-explorer
```

### Entrata

Un filone entra in DI in due modi:

1. **Da Source Observatory** — dopo un `source-check` con verdetto `go intake`, il team apre una issue in `dataset-incubator` (label `intake`) usando il template `new-candidate.yml`. La issue è collegata alla Discussion `Domanda` che ha originato lo scouting.

2. **Proposta diretta** — chiunque può aprire una issue con lo stesso template; se è abbastanza matura, riceve la label `intake` e il flusso prosegue.

### Processamento

1. **Valutazione intake** — si verifica che il caso sia abbastanza stretto con `intake-candidate.md`
2. **Creazione candidate** — si crea la struttura in `candidates/<slug>/` (`dataset.yml`, `sql/`, `notes.md`)
3. **PR e run automatico** — dopo ogni merge, `pipeline.yml` esegue il candidate via `toolkit` e valida raw → clean → mart
4. **Run successivi** — si usano `run-candidate.md` per esecuzioni manuali o verifiche

### Uscita

Un filone esce da DI in tre modi:

- **`data-explorer`** — quando il dataset è pronto per una pagina pubblica su explorer.dataciviclab.org
- **repo progetto dedicata** — quando il filone merita una casa autonoma
- **archiviazione** — quando il caso non regge o non è prioritario

Il contratto tecnico resta sempre qui, non viene rimosso.

## Stato dei filoni

Ogni filone attivo è tracciato in una issue con label:

| Label | Significato |
|---|---|
| `intake` | Entrato, in valutazione |
| `incubating` | Lavoro attivo |
| `ready-for-promotion` | Pronto per il layer pubblico |
| `promoted` | Uscito verso `analisi/` |
| `support-dataset` | Base trasversale riusabile — non è un filone |

**Support dataset**: è un dataset di supporto (es. anagrafica comuni, dizionario codici) usato per join o arricchimenti. Non entra mai in `analisi/` — serve solo a chi lavora su altri filoni.

## Struttura

```text
dataset-incubator/
  .github/
    workflows/                  # GitHub Actions automatizzate
    ISSUE_TEMPLATE/            # template per issue candidate e promotion
  candidates/                  # filoni attivi e passati
  support_datasets/            # basi trasversali riusabili
  compose/                     # composizioni mart-only su più candidate
  codelists/                   # dizionari e anagrafiche di supporto
  docs/                        # standard candidate e documentazione tecnica
  registry/
    registry.json             # artifact unico (fusion ADR) — sezioni datasets/marts/signals/codelists/entities
  templates/
    candidate/                 # template di partenza per filone
  skills/                      # skill markdown (riferimento umano per agenti e operatori)
  scripts/                     # build, validazione, push artifact
  tests/                       # test per script e validazione
  out/                         # output runtime — mai versionato
```

## Pattern di struttura

**Single-source** — una fonte sola:

```text
candidates/<slug>/
  dataset.yml
  notes.md
  sql/
    clean.sql
    mart.sql
```

**Multi-source** — più fonti indipendenti + compose:

```text
candidates/<slug>/
  notes.md
  sources/
    <fonte-a>/
      dataset.yml
      sql/clean.sql, mart.sql
    <fonte-b>/
      ...
  compose/
    dataset.yml
    sql/mart_compose.sql
```

## Workflow e azioni

I processi ricorrenti vivono sia come workflow markdown (per umani e agenti) sia come GitHub Actions (per l'esecuzione automatica):

### GitHub Actions

| Action | Trigger | Cosa fa |
|---|---|---|
| `check.yml` | PR e push su `main` | Lint + mypy + test (`python-ci`) e preflight dei dataset cambiati (`dataset-config-check-reusable`) |
| `pipeline.yml` | Merge su `candidates/`, `compose/`, `support_datasets/` + dispatch | `pipeline-reusable`: detect, run (`make run-batch`), sync GCS, registry PR |
| `smoke-weekly.yml` | Schedule settimanale | Probe di raggiungibilità fonti + verifica `registry.json` |

I due workflow di pipeline chiamano i componenti condivisi di
[`dataciviclab/.github`](https://github.com/dataciviclab/.github) (ADR-001):
niente logica nei file YAML del repo.

### Skill markdown

| Skill | Quando usarli |
|---|---|
| `intake-candidate.md` | Valutare se un caso è maturo per entrare in DI |
| `run-candidate.md` | Esecuzione manuale end-to-end o recovery |
| `post-merge-candidate.md` | Checklist del maintainer dopo il merge (run, GCS push, clean catalog) |

### Cross-repo

| Risorsa | Dove | Quando |
|---|---|---|
| `add-to-explorer` | `data-explorer` | Quando un dataset è pronto per una pagina pubblica |

## Regole operative

- Massimo 2-3 filoni attivi alla volta
- Ogni filone ha: domanda, dataset, output minimo, criterio di uscita
- I filoni escono verso `data-explorer` quando il dato è stabile e la domanda è pubblica
- I support dataset non entrano mai in `analisi/`

## Runtime locale

Gli output del toolkit vivono sotto `out/` — non vanno mai versionati. Il contenuto della repo è in `candidates/`, `support_datasets/` e `registry/`.

## Lab Clean Registry

I dataset pubblici del Lab sono tracciati in `registry/registry.json`. Per aggiornarlo:

```bash
toolkit registry build --write
```

## Per contribuire

- [CONTRIBUTING.md](CONTRIBUTING.md) — regole per issue, PR e struttura candidate
- [skills/README.md](skills/README.md) — indice degli skill e quando usarli
