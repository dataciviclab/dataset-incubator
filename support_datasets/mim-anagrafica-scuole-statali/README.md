# MIM anagrafica scuole statali

## Ruolo

Support dataset riusabile per i filoni MIM che richiedono una chiave geografica a
partire da `CODICESCUOLA`.

## Dataset

- fonte: Ministero dell'Istruzione e del Merito (MIM)
- area catalogo: `Scuole`
- file v0 intake: `SCUANAGRAFESTAT20242520250831.csv`
- URL verificato: `https://dati.istruzione.it/opendata/opendata/catalogo/elements1/SCUANAGRAFESTAT20242520250831.csv`
- licenza dichiarata: `IODL 2.0`

## Perché vale come support dataset

- espone `CODICESCUOLA` con regione, provincia e comune
- rende possibile il join geografico per `mim-alunni-corso-eta`
- può servire anche per altri filoni MIM su scuole statali

## Output minimo atteso

- tabella mart con una riga per `CODICESCUOLA`
- campi geografici e descrittivi minimi per i join
- perimetro v0 limitato all'anno scolastico `2024/25`

## Stato

- intake
- pensato come base di join, non come filone narrativo autonomo

## Prossimo passo

- verificare run reale e shape del mart
- usarlo come support dichiarativo nel candidate `mim-alunni-corso-eta`
