# Notes

## Tecnico

- caso derivato da `datasets-testing/preprojects/multi_year_schema/case_15_dipendenti_pubblici_2021_2023`
- il caso originale nasceva come test per `inspect schema-diff`, non come progetto analitico
- il feed pubblico BDAP/RGS risponde sui tre anni `2021-2023` con pattern URL stabile
- l'header 2023 differisce leggermente da 2021-2022 nella formattazione finale, ma non nel contenuto logico
- i CSV non sono UTF-8 puliti: per alcune letture locali serve `cp1252`

## Analitico

- tra 2021 e 2023 i dipendenti totali crescono
- nel 2023 assunzioni e cessazioni mostrano un saldo nettamente piu favorevole
- `Istruzione e ricerca` e `Sanita` trainano gia una parte rilevante della crescita
- i comparti sembrano gia sufficienti per una prima lettura pubblica forte

## Cautele

- non partire da ranking ente per ente: rischio inventario troppo dispersivo
- non estendere subito lo storico finche il perimetro 2021-2023 non regge da solo
- verificare se il primo output migliore e stock/turnover per comparto oppure composizione di genere

## Stato branch

- `run all` completato con esito positivo su `2021-2023`
- notebook `v0` pronto come primo pacchetto analitico

## Handoff

- promosso a `dataciviclab/analisi/dipendenti-pubblici`
- issue pubblica di passaggio: `dataciviclab#131`
- il pacchetto tecnico non viene piu mantenuto qui
