# Notes

## Tecnico

- Fonte raw: endpoint XLSX Terna `CapacityRenewableSources` con `filterMonth=12`
- Sheet letto: `Export`
- Colonne osservate nel workbook: `Anno`, `Tipo capacita`, `Regione`, `Provincia`, `Fonti`, `Potenza efficiente (MW)`
- Ultima riga del file e un footer testuale `Applied filters...` da scartare in clean
- Il clean mantiene la granularita provinciale e sia `Netta` sia `Lorda`
- Il mart v0 restringe a `Tipo capacita = Netta` e aggrega per `anno`, `regione`, `fonti`
- Run reale eseguito con successo su `2023` e `2024`
- Shape osservate:
  - clean 2023: `1160` righe
  - clean 2024: `1070` righe
  - mart 2023: `100` righe (21 con null potenza_totale_mw)
  - mart 2024: `100` righe (2 con null potenza_totale_mw)
- Notebook v0 eseguito e salvato con output leggeri, senza blob grafici
- **Lorda = Netta**: delta 0.0000% confermato su entrambi gli anni — stesso comportamento di `terna-electricity-by-source`

## Analitico

- Il candidate descrive capacita installata, non produzione
- Il confronto minimo 2023-2024 serve solo a vedere distribuzione territoriale e ordine di grandezza
- Eventuali letture su divari o performance andranno motivate solo in `analisi/`

## Cautele

- La serie storica completa non e ancora estesa oltre il biennio intake
- I valori nulli in `Potenza efficiente (MW)` vanno trattati come dato mancante, non zero implicito
- `Netta` e `Lorda` non vanno sommate tra loro
- I null in `potenza_mw` (clean) propagano al `SUM` in mart: le righe con null nel mart non sono errori ma combinazioni regione/fonte senza capacita installata dichiarata da Terna

## QC 2026-05-01

Pipeline raw→clean→mart verificata:
- Colonne raw (6): Anno, Tipo capacita, Regione, Provincia, Fonti, Potenza efficiente (MW) — tutte presenti in clean come anno, tipo_capacita, regione, provincia, fonti, potenza_mw
- 1 riga filtrata in clean (footer Applied filters...) per entrambi gli anni
- Mart aggrega per anno, regione, fonti (Netta) con sum(potenza_mw)

| Anno | raw rows | clean rows | filtered | mart rows | duplicati | delta % | null potenza_mw clean | null potenza_totale_mw mart |
|---|---|---|---|---|---|---|---|---|
| 2023 | 1161 | 1160 | 1 | 100 | 0 | 0.0000% | 363 | 21 |
| 2024 | 1071 | 1070 | 1 | 100 | 0 | 0.0000% | 157 | 2 |