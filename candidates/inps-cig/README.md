# INPS Cassa Integrazione Guadagni — Serie storiche annuali

## Domanda

Dove si concentra l'utilizzo della Cassa Integrazione in Italia? Quali province e quali settori
assorbono più ore, e come è cambiato il quadro nelle crisi recenti (2008-2012, pandemia 2020-2021)?

> Una domanda civica valida ha una tensione ("sta migliorando o peggiorando?", "c'è un divario?"),
> non è puramente descrittiva ("quanti sono") ed è verificabile con i dati disponibili.

## Dataset

- fonte: INPS Open Data — Osservatorio sulle Ore autorizzate di Cassa Integrazione Guadagni
- serie storiche annuali: https://servizi2.inps.it/docallegati/Mig/OpenData/SerieStoricheAnnualiINPS.csv
- CKAN: dati.gov.it, dataset `bef11a2c-300b-4578-8143-c1ce08f46fff`
- licenza: Creative Commons Attribuzione 4.0 Internazionale (CC BY 4.0)
- copertura: 2005–2024 (serie storica annuale)
- granularità: anno, prestazione (Ordinaria/Straordinaria/CIGD/CIGS), settore, sotto-settore
- metriche: ore autorizzate operai, ore autorizzate impiegati, totale ore autorizzate
- codifica: `;` (punto e virgola), `.` per valori nulli o zerocampi

## Perché vale la pena testarlo

- tema civico ad alta rilevanza: CIG come termometro della crisi industriale e pandemica
- serie storica lunga (20 anni) permette analisi di trend strutturale
- granularità settoriale utile per confronti tra comparti
- la pandemic 2020-2021 è visibile come spike netto nella serie

## Output minimo atteso

- raw: download CSV INPS, 2005–2024
- clean: tabella normalizzata (anno, prestazione, settore, sotto-settore, ore operai, ore impiegati, totale ore)
- mart: aggregati annui per prestazione e settore, con quota relativa
- notebook v0: esplorazione trend 2005–2024 per prestazione e settore

## Criterio di promozione

- perimetro v0 confermato: serie annuale con breakdown prestazione/settore
- trend 2005–2024 leggibile a livello di prestazione (Ordinaria vs Straordinaria)
- eventuali rotture nella serie (cambio classificazione ATECO, ecc.) documentate

## Note tecniche

- il CSV usa `;` come delimitatore e `.` come valore nullo (punti campi vuoti)
- le righe "Totale" per ogni raggruppamento vanno filtrate nel clean se si vuole solo il dettaglio settoriale
- la classificazione settoriale segue il codice statistico INPS (non ATECO verbatim, ma derivato)
- `settore_specifiche` contiene sia sotto-settori reali che totali parziali (`Totale`)

## Stato

- intake

## Prossimo passo

- probe del CSV + scaffold sql/clean.sql + run raw → verificare la struttura reale delle colonne