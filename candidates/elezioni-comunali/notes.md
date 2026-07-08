# elezioni-comunali

## Issue
DataCivicLab/dataset-incubator#633

## Fonte dati
Eligendo — https://elezionistorico.interno.gov.it/
Open data DAIT: https://dait.interno.gov.it/elezioni/open-data

## Schema raw
Colonne variabili per anno (normalizzate via COL_MAP regex):
- regione, provincia, comune, turno, elettori, votanti, lista, voti_lista, seggi_lista,
  cognome, nome, data_nascita, sesso, cod_tipo_elettore, voti_candidato

## Formato fonti
- 2016-2021: CSV/TXT in ZIP
- 2022-2023: XLSX (non gestito dal preprocess.py corrente)

## Encoding
UTF-8 con BOM o ISO-8859-1, delimitatore punto e virgola.

## Note
- Non tutti i comuni votano ogni anno: ogni comune ha elezioni ogni 5 anni.
  La copertura annuale varia (606 comuni nel 2020 causa COVID, 3.653 nel 2019).
- 2022 e 2023 hanno dati in formato XLSX su Eligendo, coprono elezioni parziali
  e straordinarie. Da implementare lettura XLSX nel preprocess.py.
