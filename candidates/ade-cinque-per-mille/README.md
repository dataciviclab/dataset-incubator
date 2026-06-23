# ade-cinque-per-mille

Dataset del 5x1000 dell'Agenzia delle Entrate: elenco enti beneficiari con
importi erogabili, per anno.

## Dati

- **Fonte**: Agenzia delle Entrate — 7 file CSV per anno (partizioni)
- **Copertura**: 2022–2025 (4 anni)
- **Record**: 41.310 (2022), 80.597 (2023), 90.611 (2024), 95.983 (2025)
- **Importo totale 2025**: ~601M€
- **Colonne clean**: 19 (anno, progressivo, codice fiscale, denominazione,
  regione, provincia, comune, 7 flag categoria, numero scelte, 4 importi)
- **Licenza**: CC-BY 4.0

## Join possibili

- `codice_fiscale` → RUNTS, anagrafe enti terzo settore
- `regione` → ISTAT demografia, ISTAT PIL territoriale
- SIOPE entrate regionali
