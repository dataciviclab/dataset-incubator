# dataset-incubator

Repo privata del core team per incubazione leggera di dataset candidati e basi trasversali del Lab.

Questa repo serve a validare filoni ancora non pronti per il flusso pubblico completo, restringere domanda e output minimo, e decidere se promuoverli verso `dataciviclab/preanalysis` o una repo progetto dedicata.

Non serve per:

- backlog indefinito
- test puramente engine del `toolkit`
- filoni gia promossi altrove
- contenuti editoriali o community ops

## Regole operative

- tenere vivi al massimo 2-3 filoni davvero attivi
- ogni filone deve avere domanda, dataset, output minimo e criterio di uscita
- se un filone e pronto, esce da qui
- i dataset trasversali non entrano in `preanalysis` per default

## Stato dei filoni

Ogni filone attivo ha una issue con label di stato:

- `intake` — entrato, source-check non ancora completato
- `incubating` — lavoro attivo in corso
- `ready-for-promotion` — pronto per passare a `dataciviclab/preanalysis`
- `promoted` — uscito; storico in `registry/archived.md`
- `support-dataset` — base trasversale riusabile, non candidato di filone

Regola pratica:

- le **issues** sono il tracker vivo di ingresso, stato e uscita dei filoni
- l'intake entra con issue dedicata
- il passaggio fuori da DI si registra con issue o label di promozione coerente
- `registry/archived.md` resta la memoria dei filoni usciti

## Struttura

```text
dataset-incubator/
  registry/
    archived.md
  templates/
    dataset-notes.md
  preprojects/
    _template/
    project_candidates/
    support_datasets/
  out/
    data/
    logs/
```

## Pattern di struttura

I candidati seguono due pattern a seconda del numero di fonti.

**Single-source** - fonte unica, dataset.yml in root del candidato:

```text
project_candidates/caso/
  dataset.yml
  notes.md
  README.md
  sql/
    clean.sql
    mart.sql
```

**Multi-source** - piu fonti indipendenti + compose finale:

```text
project_candidates/caso/
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

Il template base in `preprojects/_template/` segue il pattern single-source.

## Regola di archiviazione

Quando un candidato viene promosso o chiuso:

- aggiornare `registry/archived.md` con motivo e target finale
- ridurre il README del candidato a traccia minima (stato, motivo, puntatore)
- i file tecnici (SQL, yml, notebook) restano come storico - non vanno rimossi
- nessun altro file del candidato va aggiornato: e storico, non operativo

## Significato delle cartelle

- `registry/`: quadro umano dei filoni attivi e archiviati
- `templates/`: note di supporto riusabili
- `preprojects/project_candidates/`: filoni con domanda e potenziale di promozione
- `preprojects/support_datasets/`: basi trasversali riusabili per join o controlli
- `preprojects/_template/`: base operativa canonica per nuovi ingressi
- `out/`: runtime locale del toolkit, mai contenuto di progetto

## Contenuto attuale

La repo parte volutamente stretta.

Il tracker operativo dei filoni attivi sono le **issues di questa repo**, con label di stato (`intake`, `incubating`, `ready-for-promotion`). La storia dei filoni usciti e in `registry/archived.md`.

In questo momento la repo contiene un mix minimo di:

- `project_candidates/`
- `support_datasets/`

Fuori dal perimetro attuale:

- `IRPEF`, gia nel flusso pubblico `dataciviclab/preanalysis`
- `SIOPE`, gia repo progetto dedicata
- casi `stress_legacy`
- casi `multi_year_schema`
- output runtime sporchi o storici da altre repo

## Relazione con le altre repo

- `dataciviclab`: hub pubblico, Discussions, issue, `preanalysis/`
- `dataset-incubator`: incubazione privata del core team
- repo progetto: lavoro su filoni gia promossi
- `_local/`: note private personali o temporanee

## Runtime locale

Gli output del toolkit vivono sotto `out/` e non devono essere versionati.

Regola pratica:

- usa `out/data/...` per il runtime reale
- usa `registry/` e le cartelle in `preprojects/` per il contenuto della repo
