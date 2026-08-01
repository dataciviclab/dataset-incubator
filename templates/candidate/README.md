# Template candidato

Questo è il template operativo canonico della repo.

Ogni nuovo ingresso in `dataset-incubator` dovrebbe partire da questa cartella, adattando:

- `README.md`
- `dataset.yml`
- `notes.md`
- `sql/clean.sql`
- `sql/mart.sql`
- `notebooks/{slug}_v0.ipynb` quando il filone beneficia di un notebook v0 di validazione

Standard di riferimento: [`docs/candidate-standard.md`](../docs/candidate-standard.md).

## Bootstrap toolkit

Per un candidate nuovo, scarica RAW e produci il profiling prima del run completo:

```bash
toolkit run raw -c candidates/<slug>/dataset.yml -y 2024
```

Poi revisiona `sql/clean.sql` (deve leggere da `raw_input`, macro standard) e `clean.read`
(deve contenere solo parsing RAW verificato), e `sql/mart.sql` (aggregazioni analitiche da
`clean_input`, non pulizia raw).

Verifica la pipeline completa:

```bash
toolkit run -c candidates/<slug>/dataset.yml --years 2024
```

`toolkit run` esegue raw → clean → mart (step default) e processa i support dataset dichiarati.
Diagnostica preventiva: `toolkit run preflight -c candidates/<slug>/dataset.yml`.

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
