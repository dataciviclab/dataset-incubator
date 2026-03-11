# Terna electricity by source 2023-2024

## Domanda

Come cambia il mix di generazione elettrica per fonte tra 2023 e 2024?

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
- prima lettura della struttura del workbook
- decisione su foglio, unita di analisi e taglio del primo clean

## Criterio di promozione

Promuovere il filone solo se:

- il feed raw e stabile su almeno due anni
- la struttura del workbook e abbastanza pulita da sostenere un clean semplice
- emerge una domanda pubblica chiara sul mix per fonte

## Stato

- intake

## Prossimo passo

- verificare il run `raw`
- ispezionare fogli e colonne del workbook
- decidere il primo output minimo del `clean`
