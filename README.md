# dataset-incubator

Repo di incubazione tecnica per i dataset candidati e le basi trasversali del Lab.

Questa repo e' la casa permanente del contratto tecnico di ogni filone: `dataset.yml`, SQL, pipeline.
Il lavoro qui serve a validare la fonte, restringere la domanda e stabilizzare l'output minimo.

Se vuoi contribuire operativamente in questa repo:

- leggi [CONTRIBUTING.md](CONTRIBUTING.md)
- vedi anche [workflows/README.md](workflows/README.md)

Non serve per:

- backlog indefinito
- test puramente engine del `toolkit`
- contenuti editoriali o community ops

## Ruolo nell'ecosistema

```
source-observatory  →  dataset-incubator  →  toolkit  →  GCS  →  data-explorer
```

I candidati arrivano principalmente da due percorsi:
- **source-observatory**: portali PA scoperti e classificati da portal-scout, promossi manualmente a intake dopo verifica
- **Discussions**: domanda civica aperta in `dataciviclab`, che identifica una fonte e avvia il ciclo di intake

Una volta qui, il contratto tecnico (`dataset.yml`, SQL, pipeline) rimane permanente — anche quando i dati vengono pubblicati altrove.

## Relazione con analisi/ e le repo progetto

Il contratto tecnico (dataset.yml, sql/, pipeline) vive qui — anche dopo che il filone
e' entrato in `dataciviclab/analisi/` o in una repo dedicata.

- `dataciviclab/analisi/`: layer pubblico del filone (README civico, notebook, Discussion collegata)
- repo progetto dedicata: per filoni che richiedono sviluppo continuativo e governance propria

`dataset-incubator` non e' un passo intermedio: e' il riferimento tecnico permanente.

## Regole operative

- tenere vivi al massimo 2-3 filoni davvero attivi
- ogni filone deve avere domanda, dataset, output minimo e criterio di uscita
- se un filone e' pronto per il layer pubblico, entra in `dataciviclab/analisi/`
- i dataset trasversali non entrano in `analisi/` per default

## Stato dei filoni

Ogni filone attivo ha una issue con label di stato:

- `intake` — entrato, source-check non ancora completato
- `incubating` — lavoro attivo in corso
- `ready-for-promotion` — pronto per il layer pubblico in `dataciviclab/analisi/`
- `promoted` — layer pubblico attivo; storico in `registry/archived.md`
- `support-dataset` — base trasversale riusabile, non candidato di filone

Regola pratica:

- le **issues** sono il tracker vivo di ingresso, stato e uscita dei filoni
- l'intake entra con issue dedicata
- il passaggio a `analisi/` si registra con issue o label di promozione coerente
- `registry/archived.md` resta la memoria dei filoni archiviati

## Struttura

```text
dataset-incubator/
  registry/
    archived.md
    clean_catalog.json
    clean_catalog.schema.json
  tools/
    clean-query-mcp/
  templates/
    dataset-notes.md
    candidate/
  candidates/
  support_datasets/
  out/
    data/
    logs/
```

## Pattern di struttura

I candidati seguono due pattern a seconda del numero di fonti.

**Single-source** - fonte unica, `dataset.yml` in root del candidato:

```text
candidates/caso/
  dataset.yml
  notes.md
  README.md
  notebooks/
    caso_v0.ipynb
  sql/
    clean.sql
    mart.sql
```

**Multi-source** - piu' fonti indipendenti + compose finale:

```text
candidates/caso/
  notes.md
  README.md
  sources/
    a_fonte/
      dataset.yml
      sql/clean.sql, mart.sql
    b_fonte/
      ...
  compose/
    dataset.yml
    sql/mart_compose.sql
```

Il template base e' in `templates/candidate/` e segue il pattern single-source.
Il notebook `v0` e' opzionale ma consigliato come sanity check del mart prima della promozione.

## Uscita da `dataset-incubator`

Quando un filone matura, puo' uscire in tre modi:

- **`dataciviclab/analisi/`**
  quando e' pronto per un primo layer pubblico: README civico, notebook leggibile, Discussion collegata
- **repo progetto dedicata**
  quando il filone diventa abbastanza ricco e autonomo da meritare una casa propria
- **archiviazione**
  quando il candidate non regge o non e' prioritario

In tutti i casi il contratto tecnico (dataset.yml, sql/) resta qui — non viene rimosso.

Checklist operativa breve:

- vedi [PROMOTION_CHECKLIST.md](PROMOTION_CHECKLIST.md)

## Regola di archiviazione

Quando un candidato viene promosso o chiuso:

- aggiornare `registry/archived.md` con motivo e target finale
- ridurre il README del candidato a traccia minima (stato, motivo, puntatore)
- i file tecnici (dataset.yml, sql/, notebook) restano come riferimento permanente

## Significato delle cartelle

- `registry/`: storia dei filoni usciti (`archived.md`) e catalogo clean pubblico (`clean_catalog.json`)
- `tools/clean-query-mcp/`: MCP read-only per interrogare i clean pubblici dal Lab Clean Registry
- `templates/`: note di supporto e template operativo (`candidate/`)
- `candidates/`: filoni con domanda e potenziale di promozione
- `support_datasets/`: basi trasversali riusabili per join o controlli
- `out/`: runtime locale del toolkit, mai contenuto di progetto

## Contenuto attuale

La repo parte volutamente stretta e contiene un mix minimo di:

- `candidates/`
- `support_datasets/`

Filoni gia' con layer pubblico in `dataciviclab/analisi/`:

- `irpef-comunale` — capacita' fiscale IRPEF per comuni e regioni
- `civile-flussi` — flussi della giustizia civile nei territori
- `dipendenti-pubblici` — dinamica del pubblico impiego per comparto
- `malasanita-struttura-mortalita` — mortalita' evitabile e dotazione sanitaria
- `terna-electricity-by-source` — mix elettrico italiano per fonte

Fuori dal perimetro attuale:

- `SIOPE`, gia' repo progetto dedicata

## Relazione con le altre repo

- `dataciviclab`: hub pubblico, Discussions, issue, `analisi/`
- `dataset-incubator`: contratto tecnico permanente dei filoni
- repo progetto: lavoro su filoni con sviluppo continuativo

## Runtime locale

Gli output del toolkit vivono sotto `out/` e non devono essere versionati.

Regola pratica:

- usa `out/data/...` per il runtime reale
- usa `registry/` e le cartelle `candidates/`, `support_datasets/` per il contenuto della repo

## Lab Clean Registry

Il catalogo dei clean pubblici vive in:

- `registry/clean_catalog.json`
- `registry/clean_catalog.schema.json`

Per normalizzare il catalogo:

```bash
python scripts/build_clean_catalog.py --write
```

Per verificare anche i path GCS pubblici:

```bash
python scripts/build_clean_catalog.py --check-gcs
```

## Workflow pubblici del repo

I workflow ricorrenti e propri di `dataset-incubator` stanno in:

- [workflows/README.md](workflows/README.md)

Per ora:

- [intake-candidate.md](workflows/intake-candidate.md)
- [run-candidate.md](workflows/run-candidate.md)
