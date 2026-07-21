# Note tecniche — intercettazioni

## Raw
- File XLSX unico multi-anno
- 3 sheet: "Read me" (metadati), "Tutti gli uffici" (v0), "Tipologia di reato" (v1)
- v0: 3.953 righe, v1: 3.589 righe

## Clean
- Sheet "Tutti gli uffici": colonne Anno, Tipo ufficio, Distretto, Tipologia di intercettazione, Numero di bersagli
- Sheet "Tipologia di reato": aggiunge la colonna "Tipologia di reato"
- Procure: ordinaria + minorenni + generale

## Mart
- Aggregazione per distretto e tipologia

## Da fare
- [ ] Verificare sheet_name esatto (spazi? accenti?)
- [ ] Run v0 su anno campione (solo "Tutti gli uffici")
- [ ] v1: unire anche sheet "Tipologia di reato"
- [ ] Notebook esplorativo: trend nazionale, mappa per distretto
