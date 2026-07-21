# Note tecniche — intercettazioni

## Raw
- File XLSX unico multi-anno (2014-2025 + anni isolati 1994, 2011)
- 3 sheet: "Read me" (metadati), "Tutti gli uffici" (v0, 3.953 righe), "Tipologia di reato" (v1, 3.589 righe)
- Sheet "Tutti gli uffici": colonne verificate — Anno, Tipo ufficio, Distretto, Tipologia di intercettazione, Numero di bersagli

## Clean
- Clean v0: solo sheet "Tutti gli uffici"
- "Tipologia di intercettazione" ha valori: "Bersagli Intercettazioni Telefoniche", "Bersagli Intercettazioni Ambientali", "Bersagli Intercettazioni Informatiche", "Bersagli Intercettazioni Trojan"
- Procure: ordinaria + minorenni + generale (26 distretti)

## Mart
- Aggregazione per distretto e tipologia

## Da fare
- [x] Run v0 su anno campione (2025) — 3.953 righe OK
- [ ] v1: unire anche sheet "Tipologia di reato" (distinzione DDA/ordinaria/terrorismo)
- [ ] Notebook esplorativo: trend nazionale, mappa per distretto
