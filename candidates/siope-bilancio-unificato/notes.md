# Note tecniche — siope-bilancio-unificato

## Fonte

Parquet generato da [open-siope](https://github.com/dataciviclab/open-siope),
pubblicato su GCS pubblico:
`https://storage.googleapis.com/dataciviclab-mart/siope/siope_cross_comparto/{year}/siope_bilancio_unificato.parquet`

Il dato upstream proviene dai download open di [SIOPE](https://www.siope.it).

## Perimetro

- 2021-2026
- Entrate + uscite di tutti i comparti SIOPE
- ~18.000 enti, ~13M righe/anno
- Granularità mensile (periodo 01..12)

## Join e arricchimento

Tutti i join (territorio, comparto, classificazione voci) sono già stati
eseguiti a monte in open-siope. Il dato downstream è già arricchito.

## Rischi

- Il path GCS (`dataciviclab-mart/siope/siope_cross_comparto/`) è un contratto
  con open-siope. Se cambia, il candidate si rompe.
- I dati SIOPE vengono aggiornati mensilmente dalla fonte. Il candidate va
  rieseguito periodicamente per avere i dati freschi.

## Decisioni

- Clean e mart sono pass-through: il dato è già pulito a monte.
- Non ci sono notebook perche' il dataset e' già analitico (si puo' interrogare
  direttamente via clean-query).
