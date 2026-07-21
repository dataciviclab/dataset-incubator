# Note tecniche — penale-flussi

## Raw
- Due file XLSX: 2005-2013 (storico) e 2014-2025 (principale)
- Da verificare se i due file hanno lo stesso schema colonne
- `sheet_name` da confermare all'apertura del file (ipotesi: "Data")

## Clean
- Schema ipotizzato analogo a `civile_flussi`: anno, fonte, tipo_ufficio, distretto, sede, macromateria, materia, iscritti, definiti, pendenti
- Da riconciliare con le colonne reali del file

## Da fare
- [ ] Aprire XLSX e verificare sheet_name e colonne
- [ ] Unire i due file (2005-2013 + 2014-2025) in clean.sql
- [ ] Allineare schema a civile_flussi per join
- [ ] Run v0 su anno campione
