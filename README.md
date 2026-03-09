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

## Struttura

```text
dataset-incubator/
  registry/
    active.md
    archived.md
  templates/
    preproject.md
    dataset-notes.md
  preprojects/
    _template/
    project_candidates/
    support_datasets/
  out/
    data/
    logs/
```

## Significato delle cartelle

- `registry/`: quadro umano dei filoni attivi e archiviati
- `templates/`: template minimi riusabili
- `preprojects/project_candidates/`: filoni con domanda e potenziale di promozione
- `preprojects/support_datasets/`: basi trasversali riusabili per join o controlli
- `preprojects/_template/`: base minima per nuovi ingressi
- `out/`: runtime locale del toolkit, mai contenuto di progetto

## Cosa c'e nella v1

La repo parte volutamente stretta:

- `project_candidates/civile-flussi`
- `support_datasets/popolazione-istat-comunale-2019-2025`

Fuori dalla v1:

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
