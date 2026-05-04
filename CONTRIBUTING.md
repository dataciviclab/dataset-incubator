# Contributing to dataset-incubator

Questa guida vale per la repo `dataset-incubator`.

Per le regole GitHub condivise dell'organizzazione, parti prima da
[`.github`](https://github.com/dataciviclab/.github).

Skill pubblici del repo:

- [skills/README.md](skills/README.md)
- [skills/intake-candidate.md](skills/intake-candidate.md)
- [skills/run-candidate.md](skills/run-candidate.md)
- [skills/post-merge-candidate.md](skills/post-merge-candidate.md)

## A cosa serve questa repo

`dataset-incubator` è il luogo di intake e incubazione tecnica leggera dei
filoni dati del Lab.

Qui stanno soprattutto:

- candidate con domanda civica e potenziale di promozione
- support dataset riusabili per join o controlli
- contratto tecnico minimo del filone:
  - `dataset.yml`
  - `sql/`
  - note tecniche
  - notebook iniziali

Qui non stanno:

- docs pubbliche del Lab
- output editoriali o community ops
- feature del `toolkit`
- note personali o backlog indefinito
- filoni gia' promossi come contenuto attivo

## Quando aprire una issue qui

Apri una issue in `dataset-incubator` se il lavoro riguarda:

- intake di un nuovo candidate o support dataset
- promozione o uscita di un filone da DI
- workflow o QA interna della repo
- chiarimenti sulla struttura minima dei candidate

Template esistenti:

- `.github/ISSUE_TEMPLATE/new-candidate.yml`
- `.github/ISSUE_TEMPLATE/promotion.yml`

## Quando usare una Discussion

Se stai ancora esplorando:

- una fonte non ancora verificata
- una domanda civica ancora troppo larga
- un possible filone da stringere meglio

usa prima una `Discussion` del repo, nella category `Datasets`.

Per un source-check leggero prima di aprire una Discussion o una issue di
intake, vedi il flusso in `source-observatory`.

Quando invece hai gia' fonte, perimetro iniziale e prossimo passo concreto,
apri direttamente una issue di intake.

## Intake: come entra un nuovo filone

Usa il template `new-candidate.yml` quando vuoi proporre:

- un `candidate`
- un `support` dataset

Nel dubbio, l'intake deve avere almeno:

- domanda guida o uso previsto
- fonte principale
- perimetro iniziale stretto
- output minimo atteso
- prossimo passo concreto

Lo stato iniziale tipico è:

- label `intake`

## Stati e label di lavoro

In DI le issue sono il tracker vivo del filone.

Stati pratici:

- `intake`: ingresso iniziale, source-check o framing ancora da stringere
- `incubating`: lavoro attivo sul candidate
- `ready-for-promotion`: filone pronto a uscire da DI
- `promoted`: filone uscito verso analisi pubblica
- `support-dataset`: base trasversale, non candidate di filone

Regola pratica:

- una volta preso in carico un intake serio, il filone passa di solito da `intake` a `incubating`
- quando il passaggio fuori da DI è maturo, si apre o usa l'issue di promotion

## Struttura minima di un candidate

### Single-source

Caso piu' comune:

```text
candidates/caso/
  dataset.yml
  README.md
  notes.md
  notebooks/
    caso_v0.ipynb
  sql/
    clean.sql
    mart.sql
```

Template di partenza:

- `templates/candidate/`

Nota pratica:

- `notebooks/` non è obbligatoria per ogni intake, ma un notebook `v0` minimale è consigliato quando aiuta a validare il mart con check base prima della promozione

### Multi-source

Quando il filone ha piu' fonti indipendenti:

```text
candidates/caso/
  README.md
  notes.md
  sources/
    a_fonte/
      dataset.yml
      sql/
    b_fonte/
      dataset.yml
      sql/
  compose/
    dataset.yml
    sql/
```

Regola pratica:

- non complicare la struttura se una fonte sola basta
- usa `sources/` solo quando ci sono davvero piu' contratti tecnici separati

## Confine minimo tra clean e mart

Regola di fondo:

- `clean` serve a normalizzare il `raw`
- `mart` serve a interpretare, restringere, aggregare e leggere il dato

In `clean` sono normalmente accettabili:

- rinomina colonne
- cast e tipizzazione
- trim, normalizzazione minima di stringhe e null
- rimozione di righe spurie, header ripetuti, unita di misura o record chiaramente fuori contratto
- aggiunta di poche colonne tecniche utili a stabilizzare il dato

In `clean` non dovrebbero entrare di default:

- aggregazioni
- labeling analitico
- benchmark, cluster o categorie interpretative
- join con altre fonti
- riduzioni forti del dataset guidate gia' dalla domanda analitica

Filtri o trasformazioni piu' forti sono accettabili solo quando servono a
rendere il dato coerente con il suo contratto tecnico minimo e non con il
risultato analitico finale.

Esempi tipici di area grigia:

- dedup prudente
- esclusioni per evitare doppio conteggio
- restringimenti di perimetro gia' orientati a un compose o a un join

Quando succede, la scelta va spiegata in `notes.md` con una riga chiara:

 - che cosa viene escluso o trasformato
- perché non basta lasciarlo al `mart`
- quale rischio si evita

## Setup minimo per contribuire

La configurazione locale minima del Lab è documentata in:

- `dataciviclab/docs/local-setup.md`

Per contribuire qui ti serve soprattutto:

1. avere `dataset-incubator` e `toolkit` nello stesso workspace
2. usare una `.venv` locale funzionante
3. installare il `toolkit` in editable mode
4. saper lanciare almeno:

```bash
cd toolkit
python -m toolkit.cli.app run all --config ../dataset-incubator/candidates/{slug}/dataset.yml
```

Per candidate nested:

```bash
cd toolkit
python -m toolkit.cli.app run all --config ../dataset-incubator/candidates/{slug}/sources/{source}/dataset.yml
```

## Promotion: quando un filone esce da DI

Usa il template `promotion.yml` quando il filone sembra pronto per:

- `dataciviclab/analisi/`
- repo progetto dedicata
- archiviazione

La promotion serve a fissare:

- perché il filone è pronto a uscire
- quali artefatti esistono gia'
- quali rischi restano aperti
- quale passo concreto viene dopo

## Post-merge: GCS push e clean catalog

Dopo il merge di un candidate, il workflow `Post-Merge Candidate Registry` (GitHub Actions) apre una draft PR di handoff con la checklist dei passi manuali:

1. Run completo `toolkit run all --config candidates/{slug}/dataset.yml`
2. `python scripts/push_archive.py --layer clean --slug {slug} --create-bq-table --update-catalog --status clean_ready`
3. `python scripts/build_clean_catalog.py --write` + `--check-gcs`

Vedi [skills/post-merge-candidate.md](skills/post-merge-candidate.md) per il dettaglio completo.

## Prima di aprire una PR

- verifica se esiste gia' una issue intake o promotion collegata
- tieni il perimetro stretto
- evita di aprire candidate troppo larghi senza una domanda minima chiara
- se tocchi struttura o workflow della repo, controlla anche `README.md`
- se aggiungi o modifichi un candidate, prova almeno il `run all` o il `dry-run` piu' adatto
- se aggiungi o modifichi candidate/support dataset, esegui anche `python scripts/validate_candidate_structure.py`

## Dove orientarsi

- [README.md](README.md)
- [templates/candidate/README.md](templates/candidate/README.md)
- [.github/ISSUE_TEMPLATE/new-candidate.yml](.github/ISSUE_TEMPLATE/new-candidate.yml)
- [.github/ISSUE_TEMPLATE/promotion.yml](.github/ISSUE_TEMPLATE/promotion.yml)
