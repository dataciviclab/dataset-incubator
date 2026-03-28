# Terna electricity by source 2023-2024

> **Promosso.** Il layer pubblico vive in `dataciviclab/analisi/terna-electricity-by-source`. I file qui sotto sono storico di incubazione.

## Domanda

Come cambia tra 2023 e 2024 il peso delle diverse fonti nel mix di produzione elettrica regionale?

## Dataset

- fonte principale: export XLSX pubblico Terna `ElectricityBySource`
- copertura iniziale del preproject: dicembre 2023 e dicembre 2024
- formato sorgente: workbook `.xlsx` scaricato via HTTP
- valore del caso: possibile filone energia/ambiente con confronto semplice anno su anno

## Perche vale la pena testarlo

- e una fonte pubblica, ufficiale e gia scaricabile con URL stabile
- il confronto 2023 vs 2024 puo dare un primo output molto leggibile
- puo diventare un filone ambiente senza aprire subito un repo dedicato

## Output minimo atteso

- raw 2023 e raw 2024 scaricati con il toolkit
- clean unico del workbook `Export`
- mart regionale per fonte su produzione netta
- primo confronto 2023 vs 2024 del mix regionale
- notebook `v0` con lettura nazionale e regionale dei delta principali

## Criterio di promozione

Promuovere il filone solo se:

- il feed raw e stabile su almeno due anni
- la struttura del workbook e abbastanza pulita da sostenere un clean semplice
- emerge una domanda pubblica chiara sul mix per fonte

## Stato

- intake

## Domande complementari

- quali regioni restano piu dipendenti dal termoelettrico?
- dove cresce di piu il peso del fotovoltaico?
- quanto pesa davvero l'idroelettrico nel riequilibrio 2024?

## Prossimo passo

- eseguire `clean` e `mart`
- verificare se `lorda` e `netta` sono davvero ridondanti o solo vicine
- decidere se il primo output resta regionale o scende a livello provinciale
