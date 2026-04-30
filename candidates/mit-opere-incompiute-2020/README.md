# MIT opere pubbliche incompiute 2020

## Domanda

- Dove si concentrano le opere pubbliche incompiute nel file nazionale MIT al `31/12/2020`, e quali cause ricorrono più spesso?

## Dataset

- fonte: MIT open data, dataset `opere pubbliche incompiute al 31 dicembre 2020`
- risorsa iniziale: CSV nazionale `MIMS e regioni`
- URL pagina dataset: `https://dati.mit.gov.it/catalog/dataset/opere-pubbliche-incompiute-al-31-dicembre-2020`
- URL download CSV: `https://dati.mit.gov.it/catalog/dataset/64ea5931-39b2-47d6-9e37-41a9074dbf23/resource/e0f8b469-8d77-4c64-abca-58a17b6da82f/download/opere-incompiute-al-31-dicembre-2020mims-e-regioni.csv`
- nota: il file nazionale non copre tutte le regioni per dichiarazione esplicita della fonte; confronti regionali pieni non sono difendibili senza chiarire la copertura

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

## Stato

`runnable` — run completo eseguito, output verificati (405 righe mart), QC superato.

**QC verificati:**
- Clean = Raw: drop 4 righe (1.0%) — TOT + 3 duplicati codice_cup ✅
- Mart sum = Clean: importo_complessivo_qe coincide esattamente ✅
- 0 duplicati su codice_cup nel mart ✅
- notebook v0 compilato con output reali (14 celle, tutte popolate) ✅

## Criterio di promozione

- copertura del file nazionale chiarita in modo difendibile
- primo output leggibile su distribuzione e cause
- caveat metodologici dichiarati in modo esplicito

## Stato del candidate

- notebook `v1` aggiunto: `notebooks/mit_opere_incompiute_2020_v1.ipynb`
- tracking operativo: issue `dataset-incubator#35`

Issue collegata:
- `dataset-incubator#35`

## Prossimo passo

Post-merge: push clean a GCS, update clean_catalog, chiudere issue #35.
