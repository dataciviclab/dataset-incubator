# MIT opere pubbliche incompiute 2020

## Domanda

- Dove si concentrano le opere pubbliche incompiute nel file nazionale MIT al `31/12/2020`, e quali cause ricorrono più spesso?

## Dataset

- fonte: MIT open data, dataset `opere pubbliche incompiute al 31 dicembre 2020`
- risorsa iniziale: CSV nazionale `MIMS e regioni`
- URL pagina dataset: `https://dati.mit.gov.it/catalog/dataset/opere-pubbliche-incompiute-al-31-dicembre-2020`
- URL download CSV: `https://dati.mit.gov.it/catalog/dataset/64ea5931-39b2-47d6-9e37-41a9074dbf23/resource/e0f8b469-8d77-4c64-abca-58a17b6da82f/download/opere-incompiute-al-31-dicembre-2020mims-e-regioni.csv`

## Perche vale la pena testarlo

- tema civico forte e leggibile
- file tabellare strutturalmente pulito nel primo source-check
- presenza del `Codice_CUP` utile per dedup e possibili join futuri
- buon primo taglio su stato opera, avanzamento e cause dell'incompiutezza

## Output minimo atteso

- candidate single-source con `dataset.yml` e SQL minimi
- clean del CSV nazionale con dedup prudente su `Codice_CUP`
- mart snapshot con campi chiave e flag causa
- primo notebook `v0` su distribuzione territoriale e cause ricorrenti

## Criterio di promozione

- copertura del file nazionale chiarita in modo difendibile
- primo output leggibile su distribuzione e cause
- caveat metodologici dichiarati in modo esplicito

## Stato

- incubating

Issue collegata:
- `dataset-incubator#35`

## Prossimo passo

- verificare se il candidate deve restare sul solo file nazionale `MIMS e regioni` o includere anche file regionali separati in un secondo step
