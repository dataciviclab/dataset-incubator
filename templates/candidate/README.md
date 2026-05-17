# Template candidato

Questo è il template operativo canonico della repo.   

Ogni nuovo ingresso in `dataset-incubator` dovrebbe partire da questa cartella, adattando:

- `README.md`
- `dataset.yml`
- `notes.md`
- `sql/clean.sql`
- `sql/mart.sql`
- `notebooks/{slug}_v0.ipynb` quando il filone beneficia di un notebook v0 di validazione

## Bootstrap toolkit

Per un candidate nuovo, usa il bootstrap prima del run completo:

```bash
toolkit init --config candidates/<slug>/dataset.yml --years 2024
```

Questo scarica RAW, produce profiling e può scaffoldare/aiutare `sql/clean.sql` e `clean.read`.

Prima di lanciare `run all`, revisiona:

- `sql/clean.sql`: deve leggere da `raw_input`
- `clean.read`: deve contenere solo parsing RAW verificato
- `sql/mart.sql`: deve contenere trasformazioni analitiche, non pulizia raw

Poi verifica la pipeline completa:

```bash
toolkit run all --config candidates/<slug>/dataset.yml --years 2024
toolkit validate all --config candidates/<slug>/dataset.yml --years 2024
```

## Domanda

-
> Una domanda civica valida ha una tensione ("sta migliorando o peggiorando?", "c'è un divario?"),
> non è puramente descrittiva ("quanti sono") ed è verificabile con i dati disponibili.

## Dataset

-

## Perche vale la pena testarlo

-

## Output minimo atteso

-

## Criterio di promozione

-

## Stato

- intake

## Prossimo passo

-
