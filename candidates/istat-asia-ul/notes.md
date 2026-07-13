# Note tecniche — istat-asia-ul

## SDMX ISTAT (esploradati.istat.it) non raggiungibile

L'API SDMX di ISTAT su esploradati.istat.it non risponde (timeout).
Usiamo DBnomics come proxy per accedere ai dati ISTAT.

## Dataflow revisioni DBnomics

- `_1` (latest): Key data, REF_AREA = classi ampiezza demografica, anni 2018-2023
- `_3`: Dati territoriali completi, REF_AREA = comuni (6 cifre), anni 2018-2020
- `_4`: Solo livello paese (IT), anni 2018-2021

## API limitazioni

- DBnomics API restituisce max 1.000 serie per chiamata
- Il preprocess usa paginazione con offset per scaricare tutte le serie
- Limiti di rate non documentati; in caso di errore 429 attendere prima di riprovare

## Dimensioni stimate

- ~40 combinazioni ATECO × DATA_TYPE × circa 7.700 comuni × 3 anni ≈ 925.000 righe
- ~150-200 chiamate API totali
