# mit-incidentalita-mensile-2001-2018

Candidate - incidentalità stradale mensile in Italia, 2001-2018.

Fonte: MIT (Ministero delle Infrastrutture e dei Trasporti), portale open data.

## Stato

`runnable` — run completo eseguito, output verificati (216 righe mart), QC superato.

**Nota su `years: [2001]`**: il campo `years` in `dataset.yml` è un placeholder tecnico — il file raw è unico e copre l'intero periodo `2001-2018`.

## Perimetro

- solo righe mensili (216 su 288): le 72 righe trimestrali sono escluse per anomalie nella fonte
- copertura: 2001-2018, livello nazionale
- output minimo: `mart_mensile` con incidenti, morti, feriti, incidenti mortali e indici principali
- `morti`: campo pulito su tutta la serie; `incidenti` e `feriti`: 19 righe mensili con anomalie nella fonte MIT

## Domanda guida

Come cambia nel tempo il profilo mensile dell'incidentalita stradale in Italia tra 2001 e 2018?

## Esecuzione

```bash
python -m toolkit.cli.app run all \
  --config candidates/mit-incidentalita-mensile-2001-2018/dataset.yml
```

## Stato runtime

- `run all` completato, output verificati in `out/data/{raw,clean,mart}/mit_incidentalita_mensile/2001/`
- mart `216` righe mensili (`2001-2018`) ✅

## Note tecniche

Vedi [notes.md](notes.md) per encoding, anomalie trimestrali e cautele sugli indici derivati.
