# Note tecniche — monitoraggio-mensile-civile

## Raw
- File XLSX unico multi-anno (2019-2025)
- Sheet "Leggimi" con metadati, sheet "DATA" con i dati
- 139K righe, ~1.5MB

## Clean
- Colonne da verificare esatte: Fonte, Tipo ufficio, Anno, Mese, AnnoMese, Distretto, Sede, Materia, Iscritti, Definiti, Area, Dati
- Flag "Dati": "Consolidati" vs "Provvisori" — utile per qualità

## Mart
- Clearance rate mensile come indicatore aggiuntivo

## Da fare
- [ ] Verificare sheet_name esatto (DATA o Data o altro)
- [ ] Verificare nomi colonne reali
- [ ] Run v0 su anno campione
- [ ] Notebook esplorativo con decomposizione stagionale
