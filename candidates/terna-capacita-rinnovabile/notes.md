# Notes

## Tecnico

- Fonte raw: endpoint XLSX Terna `CapacityRenewableSources` con `filterMonth=12`
- Sheet letto: `Export`
- Colonne osservate nel workbook: `Anno`, `Tipo capacità`, `Regione`, `Provincia`, `Fonti`, `Potenza efficiente (MW)`
- Ultima riga del file e un footer testuale `Applied filters...` da scartare in clean
- Il clean mantiene la granularita provinciale e sia `Netta` sia `Lorda`
- Il mart v0 restringe a `Tipo capacità = Netta` e aggrega per `anno`, `regione`, `fonti`
- Run reale eseguito con successo su `2023` e `2024`
- Shape osservate:
  - clean 2023: `1160` righe
  - clean 2024: `1070` righe
  - mart 2023: `100` righe
  - mart 2024: `100` righe
- Notebook v0 eseguito sul mart `2024` e salvato con output leggeri, senza blob grafici

## Analitico

- Il candidate descrive capacita installata, non produzione
- Il confronto minimo 2023-2024 serve solo a vedere distribuzione territoriale e ordine di grandezza
- Eventuali letture su divari o performance andranno motivate solo in `analisi/`

## Cautele

- La serie storica completa non e ancora estesa oltre il biennio intake
- I valori nulli in `Potenza efficiente (MW)` vanno trattati come dato mancante, non zero implicito
- `Netta` e `Lorda` non vanno sommate tra loro
