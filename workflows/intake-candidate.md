# Workflow: intake-candidate

Workflow pubblico/light di `dataset-incubator`.
Versione: 0.1 - 2026-04-01

## Obiettivo di fase

Decidere se una fonte o una discussion gia' abbastanza matura puo' entrare in
`dataset-incubator` come candidate tecnico credibile.

Questo workflow serve a rispondere a:

- il caso e' abbastanza stretto per entrare in DI?
- esiste una fonte reale e un perimetro iniziale difendibile?
- l'output minimo atteso e' abbastanza chiaro?

Non serve a:

- fare puro scouting di una fonte ancora opaca
- aprire automaticamente PR o pipeline complete
- sostituire il primo source-check della fonte

## Quando usarlo

Usalo quando hai gia':

- una fonte ufficiale o una discussion abbastanza matura
- una domanda guida o un uso previsto chiaro
- un perimetro iniziale stretto
- un prossimo passo tecnico concreto

Non usarlo quando:

- la fonte e' ancora troppo larga o troppo opaca
- non sai ancora se il caso regge da solo o solo come support dataset
- manca ancora un output minimo leggibile

## Prerequisiti minimi

Prima di aprire un intake in DI dovrebbero esserci almeno:

- fonte principale verificata
- perimetro iniziale stretto
- output minimo atteso
- prossimo passo operativo concreto

Nel dubbio:

- se il caso e' ancora troppo esplorativo, resta prima in Discussion
- se il caso e' molto pulito e gia' ben definito, apri direttamente la issue di intake

## Passi minimi

### 1. Scegli il tipo di intake

Il template `new-candidate.yml` copre due casi:

- `candidate`
- `support`

Usa `candidate` quando il caso ha una domanda civica e potenziale di promozione.
Usa `support` quando il dataset serve soprattutto per join, controlli o arricchimenti.

### 2. Apri la issue di intake

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

### 3. Tieni il candidate minimale

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

Regola pratica:

- meglio un primo candidate piccolo ma eseguibile
- peggio un intake largo con perimetro ancora confuso

### 4. Chiudi l'intake con uno stato chiaro

Lo stato iniziale tipico e':

- label `intake`

Quando il filone viene preso in carico sul serio, di solito passa a:

- `incubating`

## Output minimo atteso

Un intake buono lascia:

- una issue intake chiara
- un perimetro iniziale difendibile
- un candidate o support dataset ben impostato
- issue intake e candidate coerenti tra loro
- un prossimo passo tecnico esplicito

## Dove orientarsi

- [CONTRIBUTING.md](../CONTRIBUTING.md)
- [README.md](../README.md)
- [new-candidate.yml](../.github/ISSUE_TEMPLATE/new-candidate.yml)
- [scouting-checklist.md](../docs/scouting-checklist.md)
