# Workflow: run-candidate

Workflow pubblico/light di `dataset-incubator`.
Versione: 0.1 - 2026-04-01

## Obiettivo di fase

Eseguire un candidate in `dataset-incubator` in modo end-to-end e capire se
produce output leggibili.

Questo workflow serve a rispondere a:

- quale config usare
- quale comando lanciare
- dove leggere `raw`, `clean` e `mart`
- come capire se il candidate e' andato a buon fine

Non serve a:

- fare scouting della fonte
- rifattorizzare il candidate in grande
- nascondere un blocker dietro run casuali

## Quando usarlo

Usalo quando:

- il candidate esiste gia'
- vuoi farlo girare davvero
- vuoi vedere i dati prodotti
- vuoi distinguere tra run riuscito e blocco tecnico reale

Non usarlo quando:

- il candidate non ha ancora una struttura minima
- sei ancora al livello discussion/source-check
- il lavoro vero e' ormai fix di pipeline complessa

## Workflow step-by-step

### 1. Controlla la struttura minima

Verifica che il candidate abbia almeno:

- `README.md`
- `notes.md`
- `dataset.yml` oppure config rilevanti in `sources/`

Se la struttura minima manca, fermati prima del run.

### 2. Scegli il config giusto

Chiarisci:

- se il candidate e' single-source o multi-source
- quale `dataset.yml` usare come entrypoint

Caso tipico single-source:

- `candidates/{slug}/dataset.yml`

Caso tipico multi-source:

- `candidates/{slug}/sources/{source}/dataset.yml`
- eventuale `compose/dataset.yml` come layer finale

Regola pratica:

- non partire dal compose se i source layer non sono ancora chiari

### 3. Lancia il candidate
Il run tipico usa `toolkit` sul config del candidate.

Esempio:

```bash
cd toolkit
python -m toolkit.cli.app run all --config ../dataset-incubator/candidates/{slug}/dataset.yml
```

Per candidate nested:

```bash
cd toolkit
python -m toolkit.cli.app run all --config ../dataset-incubator/candidates/{slug}/sources/{source}/dataset.yml
```

### 4. Guarda gli output

Dopo il run, controlla almeno:

- se il comando ha completato senza errori
- se il candidate ha prodotto dati sotto `dataset-incubator/out/`
- qual e' il primo file utile da aprire

In genere il percorso utile e' uno tra:

- `out/data/raw/...`
- `out/data/clean/...`
- `out/data/mart/...`

Il file piu' utile da guardare per primo e' quasi sempre il `mart`, se esiste.

### 5. Se fallisce, isola il primo errore vero

Se il run non regge, non allargare subito il lavoro.
Isola prima:

- primo errore vero
- file coinvolti
- se il blocco e' di accesso, config o SQL

Non usare questo workflow per:

- cambiare la domanda civica
- rifare il candidate da zero
- aggiungere complessita' non necessaria

## Output minimo atteso

Un run utile lascia:

- comando eseguito
- config usato
- conferma che il candidate produce output leggibili oppure primo errore vero
- primo file o layer da guardare
- prossimo passo consigliato

## Dove orientarsi

- [CONTRIBUTING.md](../CONTRIBUTING.md)
- [README.md](../README.md)
- [PROMOTION_CHECKLIST.md](../PROMOTION_CHECKLIST.md)
