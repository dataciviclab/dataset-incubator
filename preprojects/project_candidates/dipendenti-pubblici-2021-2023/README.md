# Dipendenti pubblici 2021-2023

## Domanda

Il pubblico impiego sta tornando a crescere davvero, e in quali comparti si concentra la dinamica tra 2021 e 2023?

## Dataset

- fonte: export CSV pubblico BDAP / RGS sui dipendenti pubblici per ente
- copertura iniziale del preproject: `2021`, `2022`, `2023`
- granularita di base: ente / comparto / categoria
- campi gia utili: stock dipendenti, assunti, cessati, genere, full-time / part-time

## Perche vale la pena testarlo

- tema pubblico molto leggibile
- buona base per misurare crescita, turnover e composizione dei comparti
- il perimetro 2021-2023 e gia sufficiente per un primo output senza aprire subito uno storico piu lungo

## Output minimo atteso

- mart per anno e comparto con:
  - dipendenti totali
  - assunti
  - cessati
  - saldo netto
  - quota donne
- prima lettura dei comparti che trainano la crescita 2021-2023

## Criterio di promozione

Promuovere il filone solo se:

- il mart minimo produce una storia leggibile, non solo un inventario
- emerge almeno un confronto forte tra comparti
- il perimetro 2021-2023 regge senza richiedere subito un'estensione storica

## Stato

- intake

## Prossimo passo

- eseguire `run all`
- verificare se il primo output migliore e per comparto, per tipo istituzione o per genere
- tenere `inputs/` solo come fallback locale se il feed pubblico cambia o si rompe
