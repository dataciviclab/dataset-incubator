# ade-cinque-per-mille

Dataset del 5x1000 dell'Agenzia delle Entrate: elenco enti beneficiari con
importi erogabili, per anno.

## Dati

- **Fonte**: Agenzia delle Entrate — 7 file CSV per anno (partizioni)
- **Copertura**: 2024 (v0)
- **Record**: 90.611 enti
- **Importo totale**: ~522M€
- **Colonne clean**: 19 (anno, progressivo, codice fiscale, denominazione,
  regione, provincia, comune, 7 flag categoria, numero scelte, 4 importi)
- **Licenza**: CC-BY 4.0

## Join possibili

- `codice_fiscale` → RUNTS, anagrafe enti terzo settore
- `regione` → ISTAT demografia, ISTAT PIL territoriale
- SIOPE entrate regionali
