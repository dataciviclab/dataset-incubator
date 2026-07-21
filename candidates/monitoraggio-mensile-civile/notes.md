# Note tecniche — monitoraggio-mensile-civile

## Raw
- File XLSX unico multi-anno (2019-2025), ~1.5MB
- 2 sheet: "Leggimi" (metadati), "DATA" (139.114 righe × 12 colonne)
- Colonne verificate: Fonte, Tipo ufficio, Anno, Mese, AnnoMese, Distretto, Sede, Materia, Iscritti, Definiti, Area, Dati

## Clean
- 139.114 righe → 139.114 righe clean (nessuna filtrada)
- Anno è INTEGER, Mese è STRING ('01', '02', ...)
- Flag "Dati": "Consolidati" vs "Provvisori" — utile per qualità

## Mart
- Clearance rate mensile aggregato per distretto e area

## Da fare
- [x] Run v0 su anno campione (2025) — 139.114 righe OK
- [ ] Notebook esplorativo con decomposizione stagionale
- [ ] Verificare distribuzione flag consolidati/provvisori nel tempo
