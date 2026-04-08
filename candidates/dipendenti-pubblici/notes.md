# Notes

## Tecnico

- caso derivato da `datasets-testing/preprojects/multi_year_schema/case_15_dipendenti_pubblici_2021_2023`
- il caso originale nasceva come test per `inspect schema-diff`, non come progetto analitico
- il feed pubblico BDAP/RGS risponde su tutti gli anni `2010-2023` con pattern URL stabile
- nessun drift di schema rilevato tra 2010 e 2023: stesse colonne, stesso encoding `cp1252`
- i CSV non sono UTF-8 puliti: per alcune letture locali serve `cp1252`

## Analitico

- tra 2010 e 2023 la serie permette di leggere cicli di espansione e contrazione per comparto
- tra 2021 e 2023 i dipendenti totali crescono; nel 2023 il saldo assunzioni/cessazioni è nettamente positivo
- `Istruzione e ricerca` e `Sanita` trainano una parte rilevante della crescita recente
- i comparti sono sufficienti per una lettura pubblica forte sia sulla serie storica che sull'ultimo triennio

## Cautele

- non partire da ranking ente per ente: rischio inventario troppo dispersivo
- non partire da ranking ente per ente sulla serie lunga: rischio di dispersività
- verificare se il primo output migliore e stock/turnover per comparto oppure composizione di genere

## Stato branch

- `run all` completato con esito positivo su tutti i 14 anni `2010-2023`
- notebook `v0` pronto come primo pacchetto analitico

## Handoff

- promosso a `dataciviclab/analisi/dipendenti-pubblici`
- issue pubblica di passaggio: `dataciviclab#131`
- il pacchetto tecnico non viene piu mantenuto qui
