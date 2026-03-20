# mit-incidentalita-mensile-2001-2018

Candidate - incidentalita stradale mensile in Italia, 2001-2018.

Fonte: MIT (Ministero delle Infrastrutture e dei Trasporti), portale open data.

## Stato

`incubating` - candidate strutturato, con verifica tecnica del `run all` riportata in issue e artefatti runtime non versionati nella repo.

Issue: dataciviclab/dataset-incubator#34

## Perimetro

- solo righe mensili (216 su 288): le 72 righe trimestrali sono escluse per anomalie nella fonte
- copertura: 2001-2018, livello nazionale
- output minimo: `mart_mensile` con incidenti, morti, feriti, incidenti mortali e indici principali

## Domanda guida

Come cambia nel tempo il profilo mensile dell'incidentalita stradale in Italia tra 2001 e 2018?

## Esecuzione

```bash
python -m toolkit.cli.app run all \
  --config candidates/mit-incidentalita-mensile-2001-2018/dataset.yml
```

## Stato runtime

- verifica tecnica riportata in issue con `run all` completato
- output atteso del mart minimo: `216` righe mensili (`2001-2018`)
- gli artefatti `out/` non sono committati nella repo

## Note tecniche

Vedi [notes.md](notes.md) per encoding, anomalie trimestrali e cautele sugli indici derivati.
