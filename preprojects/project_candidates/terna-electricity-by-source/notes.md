# Notes

## Tecnico

- setup iniziale limitato al solo layer `raw`
- due snapshot espliciti: `2023`, `2024`
- sorgente HTTP Terna che restituisce direttamente workbook `.xlsx`
- file naming locale separato per anno
- workbook con un solo foglio: `Export`
- presente una riga finale di testo `Applied filters...` da scartare nel clean
- colonne rilevate: `Anno`, `Tipo produzione`, `Regione`, `Provincia`, `Fonte`, `Produzione (GWh)`

## Analitico

- domanda chiave: come cambia il peso delle fonti nel mix elettrico regionale tra 2023 e 2024?
- taglio iniziale da tenere stretto: produzione `Netta`, aggregata per `anno-regione-fonte`
- domande complementari:
  - quali regioni restano piu termoelettriche?
  - dove cresce il fotovoltaico?
  - dove l'idroelettrico sposta davvero il mix?
- non allargare subito a serie lunga o granularita territoriali

## Cautele

- l'URL Terna contiene parametri applicativi (`pageSize`, `filterMonth`) da non dare per stabili a lungo
- finche non leggiamo il workbook non fissiamo ancora foglio, schema o metrica principale
- `Tipo produzione` ha due valori (`Lorda`, `Netta`) con totale nazionale uguale nei due anni osservati: per il primo mart usiamo `Netta`, ma la ridondanza va ricontrollata prima di trarre conclusioni metodologiche
