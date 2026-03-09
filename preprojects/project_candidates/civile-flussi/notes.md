# Notes

## Tecnico

- workbook reale con foglio descrittivo `Read me` e foglio dati `data`
- caso utile per testare `clean.read.sheet_name` su `.xlsx`
- il contenuto copre piu anni nel file stesso (`2014`-`2024`)
- `years: [2024]` e usato come chiave di snapshot del run e del path output, non come filtro dei dati
- il run del toolkit resta oggi sul year-dir del caso
- stato tecnico atteso: `OK`
- fonte diretta: file XLSX pubblico del Ministero della Giustizia / dati e statistiche

## Analitico

- tema forte: carico della giustizia civile nel tempo
- vantaggio principale: combinazione di serie storica e confronto territoriale
- rischio principale: troppi possibili tagli analitici insieme
- primo output da tenere stretto: trend + confronto territoriale selezionato
- cautela: classificazione modificata nel tempo, soprattutto dal 2021 e dal 2022

## Cautele

- evitare letture troppo fini per materia su tutta la serie
- non allargare il primo output prima di fissare un'unita di confronto leggibile
