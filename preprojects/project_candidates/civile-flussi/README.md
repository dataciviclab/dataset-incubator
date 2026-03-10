# Civile flussi 2014-2024

## Stato

Promosso. Il lavoro vivo e in `dataciviclab/preanalysis/civile-flussi-2014-2024`.
Questo candidato non e piu attivo in `dataset-incubator`.

## Motivo della promozione

- run e2e stabile sul file reale (XLSX Ministero Giustizia, 2014-2024)
- struttura del dato consente confronti leggibili (serie storica + confronto territoriale)
- domanda analitica fissata: il carico della giustizia civile sta migliorando o peggiorando nei territori?

## Traccia tecnica

- fonte: `CivileFlussi20142024.xlsx` (Ministero della Giustizia / dati e statistiche)
- copertura: 2014-2024 nel file sorgente; `years: [2024]` usato come chiave di snapshot del run
- nota struttura: foglio `data` + foglio descrittivo `Read me`; classificazione modificata dal 2021 (tribunale imprese) e dal 2022 (CCII)
- sql, yml e notebook D1 restano come riferimento storico del lavoro in incubator

## Riferimento attivo

`dataciviclab/preanalysis/civile-flussi-2014-2024`
