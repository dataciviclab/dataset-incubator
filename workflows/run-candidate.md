---
name: run-candidate
description: Workflow canonico di dataset-incubator per eseguire un candidate, verificare gli output e chiudere con uno stato tecnico chiaro.
license: MIT
metadata:
  version: "0.2"
  owner: "DataCivicLab"
  tags: [dataset-incubator, run, candidate, validation]
---

# Workflow: run-candidate

Workflow canonico di `dataset-incubator`.
Versione: 0.2 - 2026-04-08

## Obiettivo di fase

Eseguire un candidate in `dataset-incubator` in modo reale e capire, in modo
disciplinato, se:

- il candidate gira davvero
- i layer `raw`, `clean` e `mart` vengono prodotti
- gli output risultano leggibili
- il problema, se c'e', e' un blocker tecnico chiaro oppure solo rumore

Questo workflow serve a:

- scegliere il config giusto
- fare un run reale o il minimo check eseguibile
- capire dove guardare gli output
- distinguere tra `runnable`, `scaffolded_with_blocker` e `wait`

Non serve a:

- fare scouting di una fonte ancora opaca
- rifare il candidate da zero
- trasformare il run in refactor largo
- nascondere un blocker dietro tentativi casuali

## Quando usarlo

Usalo quando hai gia':

- un candidate con struttura minima reale
- un `dataset.yml` chiaro da usare come entrypoint
- un motivo preciso per eseguirlo:
  - validazione tecnica
  - primo run reale
  - verifica dopo fix

Non usarlo quando:

- il candidate e' ancora nella fase di intake immaturo
- manca ancora il boundary tra `clean` e `mart`
- la fonte non e' ancora abbastanza verificata
- il lavoro vero e' ormai debugging complesso di pipeline e richiede un workflow piu' stretto

## Preconditions minime

Prima del run dovrebbero esserci almeno:

- slug del candidate
- config entrypoint chiaro
- accesso al repo `toolkit`
- aspettativa minima su cosa dovrebbe produrre il run
- candidate esistente in `candidates/{slug}/`
- `dataset.yml` presente e coerente col layer che vuoi eseguire
- `sql/` presenti se il candidate prevede `clean` e `mart`
- un `README.md` o `notes.md` che dica almeno qual e' il perimetro

Nel dubbio:

- se il candidate non ha ancora una forma minima verificabile, fermati e torna prima al workflow di intake

## Stop rules

Fermati e non forzare il run quando:

- il candidate non ha ancora una struttura minima
- non e' chiaro quale config sia l'entrypoint reale
- il problema e' ancora di fase precedente:
  - scouting
  - source-check
  - boundary del candidate
- il `clean` e' gia' un mart travestito e il run starebbe solo nascondendo il problema
- dopo un primo errore reale stai gia' cambiando troppe cose insieme senza aver isolato il blocker

## Passi canonici

### 1. Controlla la struttura minima

Verifica che il candidate abbia almeno:

- `README.md`
- `notes.md`
- `dataset.yml`

e, se previsti:

- `sql/clean.sql`
- `sql/mart.sql`
- notebook v0

Se manca la struttura minima, fermati prima del run.

### 2. Scegli l'entrypoint giusto

Chiarisci subito quale config vuoi eseguire.

Caso tipico single-source:

- `candidates/{slug}/dataset.yml`

Caso tipico multi-source:

- `candidates/{slug}/sources/{source}/dataset.yml`
- eventuale `compose/dataset.yml` come layer finale

Regola pratica:

- non partire dal compose se i source layer non sono ancora chiari o verificati
- se non hai un motivo specifico per fare altro, parti da `run all` sul `dataset.yml` principale del candidate

### 3. Fai prima un controllo path/config

Prima di lanciare tutto, verifica almeno:

- che il config punti ai path attesi
- che `root` e cartelle di output siano coerenti
- che il candidate non stia leggendo o scrivendo in percorsi inattesi

Se il contract dei path non e' chiaro, fermati prima del run completo.

Se il server MCP `toolkit` e' attivo nel runtime:

- `toolkit_inspect_paths(config_path)` - alternativa al controllo manuale di path e contract

### 4. Lancia il run minimo giusto

Il run tipico usa `toolkit` sul config del candidate.

Esempio single-source:

```bash
cd toolkit
python -m toolkit.cli.app run all --config ../dataset-incubator/candidates/{slug}/dataset.yml
```

Esempio nested:

```bash
cd toolkit
python -m toolkit.cli.app run all --config ../dataset-incubator/candidates/{slug}/sources/{source}/dataset.yml
```

Regola:

- partire dal minimo run che risponde alla domanda tecnica del momento
- non fare subito piu' run diversi se il primo non e' ancora chiaro

### 5. Controlla gli output

Dopo il run, controlla almeno:

- se il comando e' completato senza errori
- se `raw`, `clean` e `mart` sono stati prodotti dove atteso
- qual e' il primo file utile da aprire

I percorsi tipici sono dentro:

- `out/data/raw/...`
- `out/data/clean/...`
- `out/data/mart/...`

Se esiste, il primo file piu' utile da guardare e' spesso il `mart`.

Segnale minimo di output leggibile:

- il file si apre
- non e' vuoto
- le colonne principali sono coerenti con la domanda o col layer atteso
- non ci sono rotture evidenti o valori palesemente fuori posto

Se il server MCP `toolkit` e' attivo nel runtime:

- `toolkit_blocker_hints(config_path)` - evidenzia mismatch tra output risolti e run record

### 6. Se fallisce, isola il primo errore vero

Se il run non regge:

- isola il primo errore vero
- annota file e layer coinvolti
- distingui tra:
  - accesso fonte
  - config/path
  - parsing
  - SQL
  - validazione

Se utile, chiudi il blocker con una formula semplice:

- `blocco fonte`
- `blocco config/path`
- `blocco parsing`
- `blocco SQL`
- `blocco validazione`

Non usare questo workflow per:

- cambiare la domanda civica
- allargare il candidate
- fare refactor larghi prima di aver capito il blocker

### 7. Chiudi con uno stato chiaro

Il workflow dovrebbe uscire in uno di questi stati:

- `runnable`
- `scaffolded_with_blocker`
- `wait`

Se il server MCP `toolkit` e' attivo, `toolkit_review_readiness(config_path)` esegue i check di readiness prima di passare alla review: config valida, layer presenti, output leggibili, coerenza run record.

`runnable`:

- il candidate gira davvero e produce output leggibili

`scaffolded_with_blocker`:

- la struttura regge, ma esiste un blocker tecnico preciso

`wait`:

- manca ancora un pezzo di fase precedente e non ha senso insistere col run

## Errori tipici

- partire dal config sbagliato
- lanciare `compose` troppo presto
- non controllare i path prima del run
- guardare solo il codice di uscita e non gli output reali
- cambiare troppe cose insieme dopo il primo errore
- usare il run per coprire un candidate ancora immaturo

## Output minimo atteso

Un run utile lascia:

- config usato
- esito del run
- layer prodotti o primo blocker reale
- primo file o output da guardare
- prossimo passo tecnico chiaro

## Definition of done

Il workflow e' chiuso bene quando:

- l'entrypoint usato e' chiaro
- l'esito e' classificato in modo netto
- esiste almeno un output verificato oppure un blocker tecnico preciso
- non sono stati nascosti problemi di boundary del candidate dietro il run
- il prossimo passo e' esplicito e piccolo

## Stati finali ammessi

- `runnable`
- `scaffolded_with_blocker`
- `wait`

## Dove orientarsi

- [README.md](../README.md)
- [CONTRIBUTING.md](../CONTRIBUTING.md)
- [intake-candidate.md](./intake-candidate.md)
