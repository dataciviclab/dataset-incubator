# elezioni-referendum

## Issue
DataCivicLab/dataset-incubator#633

## Fonte dati
Eligendo — https://elezionistorico.interno.gov.it/
Open data DAIT: https://dait.interno.gov.it/elezioni/open-data

## Schema raw
Colonne variabili per anno (normalizzate via COL_MAP regex):
- regione, provincia, comune, num_quesito, quesito, elettori, votanti, voti_si, voti_no, schede_bianche, ...

## Gap noti
- 1995-2006: solo livello provinciale (colonna comune NULL)
- 2011 in poi: livello comunale
- 2001: solo referendum costituzionale (Titolo V) — diverso dagli abrogativi
- Non inclusi: 2009 (dati non trovati su Eligendo)

## Note
- I quesiti multipli per anno hanno lo stesso num_quesito per tutti i comuni
- I totali voti SI+NO nei dati sono la somma per tutti i quesiti dell'anno
