---
name: intake-candidate
description: Workflow canonico di dataset-incubator per decidere se una fonte o discussion abbastanza matura puo' entrare come candidate tecnico credibile.
license: MIT
metadata:
  version: "0.2"
  owner: "DataCivicLab"
  tags: [dataset-incubator, intake, candidate, support-dataset]
---

# Workflow: intake-candidate

Workflow canonico di `dataset-incubator`.
Versione: 0.2 - 2026-04-07

## Obiettivo di fase

Decidere se una fonte o una discussion gia' abbastanza matura puo' entrare in
`dataset-incubator` come candidate tecnico credibile.

Questo workflow serve a rispondere a:

- il caso e' abbastanza stretto per entrare in DI?
- esiste una fonte reale e un perimetro iniziale difendibile?
- l'output minimo atteso e' abbastanza chiaro?
- il candidate puo' stare in DI senza sconfinare gia' in analisi?

Non serve a:

- fare puro scouting di una fonte ancora opaca
- sostituire il primo source-check della fonte
- nascondere dietro un intake un caso ancora troppo immaturo
- costruire una pipeline completa oltre il minimo tecnico necessario

## Quando usarlo

Usalo quando hai gia':

- una fonte ufficiale o una discussion abbastanza matura
- una domanda guida o un uso previsto chiaro
- un perimetro iniziale stretto
- un prossimo passo tecnico concreto
- un source-check reale oppure un equivalente leggero con verdetto esplicito

Non usarlo quando:

- la fonte e' ancora troppo larga o troppo opaca
- non sai ancora se il caso regge da solo o solo come support dataset
- manca ancora un output minimo leggibile
- il caso e' gia' troppo analisi per stare in DI
- il layer `clean` sarebbe gia' il taglio finale del mart

## Preconditions minime

Prima di aprire o consolidare un intake in DI dovrebbero esserci almeno:

- fonte principale verificata
- perimetro iniziale stretto
- output minimo atteso
- prossimo passo operativo concreto
- verdetto minimo sul source-check:
  - `go candidate`
  - oppure equivalente stretto che regga il passaggio in DI

Per `equivalente stretto` intendiamo almeno:

- fonte reale verificata
- perimetro iniziale gia' formulato
- domanda o uso previsto leggibile
- rischio tecnico principale gia' esplicitato

Nel dubbio:

- se il caso e' ancora troppo esplorativo, resta prima in Discussion o source-check
- se il caso e' molto pulito e gia' ben definito, apri la issue di intake

## Stop rules

Fermati e non forzare intake quando:

- il source-check non regge ancora il passaggio in DI
- il candidate e' gia' troppo analisi
- il `clean` e' gia' un mart travestito
- il perimetro cambia durante l'intake senza riallineamento completo di issue, README, notes, notebook e SQL
- il caso appartiene in realta' a un altro repo o a una fase successiva

## Passi canonici

### 1. Scegli il tipo di intake

Il template `new-candidate.yml` copre due casi:

- `candidate`
- `support`

Usa `candidate` quando il caso ha una domanda civica e potenziale di promozione.
Usa `support` quando il dataset serve soprattutto per join, controlli o arricchimenti.

### 2. Apri o allinea la issue di intake

Usa:

- `.github/ISSUE_TEMPLATE/new-candidate.yml`

Compila in modo stretto:

- domanda guida o uso previsto
- fonte principale
- perimetro iniziale
- perche' vale la pena incubarlo
- output minimo atteso
- prossimo passo operativo
- rischi noti

Se il candidate esiste gia', riallinea la issue al perimetro reale prima di andare avanti.

Se esiste gia' una PR o un candidate aperto sullo stesso caso:

- non aprire un doppione
- riallinea prima il perimetro reale
- chiarisci cosa stai aggiungendo o correggendo rispetto al lavoro gia' vivo

### 3. Crea la struttura minima del candidate

Nel caso single-source, la struttura tipica e':

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

Il notebook v0 si copia dal template:

```bash
cp "templates/candidate/notebooks/{slug}_v0.ipynb" "candidates/{slug}/notebooks/{slug}_v0.ipynb"
```

Poi apri il notebook e imposta i due parametri manuali in cima alla cella `setup`:

```python
METRICA       = "..."  # colonna numerica principale nel mart
METRICA_CLEAN = "..."  # colonna corrispondente nel clean
```

Il resto (slug, anni, mart table, encoding, separatore) viene letto automaticamente dal `dataset.yml`.

Regola pratica:

- meglio un primo candidate piccolo ma eseguibile
- peggio un intake largo con perimetro ancora confuso

### 4. Mantieni distinti i layer

Durante l'intake:

- `clean.sql` deve restare layer tecnico
- `mart.sql` puo' portare il taglio della domanda
- il notebook v0 deve verificare il mart reale, non anticipare gia' una mini-analisi

Se il `clean` sta gia' facendo il lavoro del mart, fermati e correggi il boundary.

### 5. Esegui il minimo tecnico necessario

Prima di chiudere l'intake, fai almeno il minimo che renda il candidate verificabile:

- verifica `root` e path effettivi
- esegui un primo run reale oppure un dry-run credibile
- se il run non regge, documenta un blocker tecnico specifico
- non lasciare blocker vaghi o formulaici

Sequenza minima consigliata, se non hai un motivo specifico per fare altro:

1. verifica path e contract del config
2. fai girare il layer `raw`
3. se `raw` regge, passa a `clean`
4. se `clean` regge, passa a `mart`
5. costruisci o aggiorna il notebook v0 sul mart reale

Esempio tipico:

```bash
cd toolkit
python -m toolkit.cli.app inspect paths --config ../dataset-incubator/candidates/{slug}/dataset.yml
python -m toolkit.cli.app run raw --config ../dataset-incubator/candidates/{slug}/dataset.yml
python -m toolkit.cli.app run clean --config ../dataset-incubator/candidates/{slug}/dataset.yml
python -m toolkit.cli.app run mart --config ../dataset-incubator/candidates/{slug}/dataset.yml
```

Se il candidate e' nested, usa il `dataset.yml` del source layer giusto.

Se il server MCP `toolkit` e' attivo nel runtime, puoi usare in alternativa alla CLI:

- `toolkit_inspect_paths(config_path)` - verifica path e contract del config
- `toolkit_blocker_hints(config_path)` - evidenzia mismatch pratici tra output risolti e stato run

Per il dettaglio del run e dei blocker, il riferimento resta:

- [run-candidate.md](./run-candidate.md)

### 6. Aggiungi sempre un notebook v0 reale

Il notebook v0 non e' opzionale.

Deve:

- essere copiato da `templates/candidate/notebooks/{slug}_v0.ipynb`
- avere `METRICA` e `METRICA_CLEAN` impostati manualmente
- girare senza errori su raw, clean e mart reali
- non restare placeholder o TODO

Il notebook valida la pipeline per fasi (raw → clean → mart) e mostra le SQL come contesto.
Non deve contenere analisi del dato: quella va in `analisi-civiche`.

### 7. Riallinea tutto se cambia il perimetro

Se durante l'intake cambia:

- granularita'
- copertura temporale
- domanda guida
- naming del candidate

allora riallinea subito:

- issue
- README
- notes
- notebook v0
- SQL
- dataset.yml

Non lasciare un candidate tecnico e un framing pubblico che raccontano due cose diverse.

### 8. Chiudi l'intake con uno stato chiaro

Lo stato iniziale tipico e':

- label `intake`

Quando il filone viene preso in carico sul serio, di solito passa a:

- `incubating`

Il candidate deve uscire almeno in uno di questi stati:

- `runnable`
- `scaffolded_with_blocker`
- `wait`

Non forzare `runnable` se il primo run non regge davvero.

## Errori tipici

- aprire intake quando il caso e' ancora troppo esplorativo
- usare un source-check troppo debole e chiamarlo comunque pronto per DI
- lasciare mismatch tra issue, `dataset.yml`, README, notes e notebook
- far fare a `clean` il lavoro che dovrebbe stare in `mart`
- lasciare il notebook v0 come placeholder invece che come check reale
- aprire o chiedere review sulla PR con perimetro ancora instabile

## Output minimo atteso

Un intake buono lascia:

- una issue intake chiara
- un perimetro iniziale difendibile
- un candidate o support dataset ben impostato
- issue intake e candidate coerenti tra loro
- un notebook v0 reale
- un prossimo passo tecnico esplicito

## Definition of done

Il workflow e' considerato chiuso bene quando:

- il candidate resta nel boundary tecnico di `dataset-incubator`
- non c'e' salto di fase nascosto in `clean`, `mart` o notebook
- esiste almeno un run verificato oppure un blocker tecnico specifico
- README, notes, notebook e mart sono coerenti sullo stesso perimetro
- non ci sono file temporanei o macchina-specifici nel candidate

## Prima di aprire o chiedere review sulla PR

Prima di considerare l'intake abbastanza sano da aprire una PR o chiedere review, controlla almeno che:

- issue intake e candidate siano coerenti
- il perimetro sia stabile abbastanza
- il notebook v0 sia reale e non placeholder
- esista almeno un run verificato oppure un blocker tecnico specifico
- il prossimo passo sia chiaro:
  - `runnable`
  - `scaffolded_with_blocker`
  - `wait`
- se il server MCP `toolkit` e' disponibile, `toolkit_review_readiness(config_path)` anticipa i check minimi di readiness: config valida, layer presenti, output leggibili, coerenza run record

## Dove orientarsi

- [CONTRIBUTING.md](../CONTRIBUTING.md)
- [README.md](../README.md)
- [new-candidate.yml](../.github/ISSUE_TEMPLATE/new-candidate.yml)
