# Notes - mit-incidentalita-mensile-2001-2018

## Stato

Candidate creato il 2026-03-20.
Issue di riferimento: dataciviclab/dataset-incubator#34.

La verifica tecnica riportata in issue indica:
- `run all` completato
- `216` righe nel `mart_mensile`
- copertura `2001-2018` coerente

Gli artefatti runtime locali non sono versionati nella repo.

## Tecnico

- URL: diretto, `200 OK`, `text/csv`, no login
- encoding effettivo gestito con `source: config_only`, `header: false`, `skip: 1`
- delimiter: `,`
- decimal nei campi percentuale/indice: `,` nel raw quoted -> `REPLACE(',', '.')`
- totale righe raw: `288` (`216` mensili + `72` trimestrali)
- copertura mensile: `18` anni x `12` mesi = `216` righe esatte
- nel notebook v0 sono emerse anche `19` righe mensili con trailing zero mancante in `incidenti` o `feriti`; `morti` resta il campo piu affidabile sull'intera serie mensile
- il campo `Mese` ha leading spaces nel raw -> `TRIM` in clean
- il campo `Anno` ha trailing space nell'header originale -> gestito con colonne esplicite

## Perimetro

Solo righe mensili. Le `72` righe trimestrali sono escluse perche:
- `8` trimestri hanno trailing zero mancante
- `5` trimestri hanno valori irregolari non recuperabili in modo difendibile

I totali annuali possono essere ricalcolati dai mesi per:
- incidenti
- morti
- feriti
- incidenti_mortali

Gli indicatori derivati MIT (mortalita, gravita, lesivita) sono prodotti sulla serie completa originale, inclusi i trimestrali. Nel mart vengono propagati come orientativi e nel notebook v0 va messa una nota esplicita.

## Colonne principali

| Campo raw | Campo clean | Note |
| --- | --- | --- |
| `Mese` | `mese` | `TRIM` |
| `Anno ` | `anno` | cast integer |
| `Incidenti` | `incidenti` | integer |
| `Morti` | `morti` | integer |
| `Feriti` | `feriti` | integer |
| `Incidenti mortali` | `incidenti_mortali` | integer |
| `Indice di mortalita generico` | `indice_mortalita` | double |
| `Indice di gravita` | `indice_gravita` | double |
| `Indice di lesivita` | `indice_lesivita` | double |

## Esecuzione

```bash
cd dataset-incubator
python -m toolkit.cli.app run all \
  --config candidates/mit-incidentalita-mensile-2001-2018/dataset.yml
```

Il `years: [2001]` in `dataset.yml` e un placeholder tecnico: il file raw e unico e copre `2001-2018`.

## Output atteso

- `mart_mensile`: `216` righe, ordinate per `anno` e `mese_num`
- validation minima: `min_rows: 200` su clean e mart

## Domanda guida

Come cambia nel tempo il profilo mensile dell'incidentalita stradale in Italia tra 2001 e 2018? Trend di lungo periodo, stagionalita, e rapporto tra incidenti totali e incidenti mortali.

## Rischi residui

- gli indici derivati MIT non sono ricalcolati dal solo mensile filtrato
- il dataset non ha granularita territoriale: e una serie temporale nazionale
- la serie si ferma al `2018`: da dichiarare esplicitamente nell'output pubblico
