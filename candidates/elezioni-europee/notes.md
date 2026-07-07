# elezioni-europee

## Issue
DataCivicLab/dataset-incubator#633

## Fonte dati
Eligendo — https://elezionistorico.interno.gov.it/
Open data DAIT: https://dait.interno.gov.it/elezioni/open-data

## File raw
10 ZIP da Eligendo (europee-YYYYMMDD.zip), ciascuno contiene un file TXT/CSV con scrutini per comune.

## Schema raw
Colonne variabili per anno (normalizzate via COL_MAP regex):
- circoscrizione, regione, provincia, comune, lista, voti_lista, elettori, votanti, schede_bianche

## Encoding
UTF-8 con BOM, delimitatore punto e virgola.

## Note
- 2019: il file `_PrefEuropee2019_LivComune.txt` contiene preferenze (voti candidato).
  Il preprocess.py filtra `_Pref*` per usare il file scrutini standard.
- 1979-2014: unico file per anno. 2024: formato con file separati per livComune e sezioni.
- Anni pre-1994 hanno meno liste (11-13) vs picco 1999-2004 (25-26).
- COL_MAP normalizza nomi colonna con regex case-insensitive.
