# Notes

## Tecnico

- setup iniziale limitato al solo layer `raw`
- due snapshot espliciti: `2023`, `2024`
- sorgente HTTP Terna che restituisce direttamente workbook `.xlsx`
- file naming locale separato per anno

## Analitico

- taglio iniziale da tenere stretto: confronto mix per fonte tra 2023 e 2024
- non allargare subito a serie lunga o granularita territoriali
- capire prima se il dataset e nazionale, territoriale o misto nel workbook

## Cautele

- l'URL Terna contiene parametri applicativi (`pageSize`, `filterMonth`) da non dare per stabili a lungo
- finche non leggiamo il workbook non fissiamo ancora foglio, schema o metrica principale
