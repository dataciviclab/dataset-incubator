# Note tecniche — penale-flussi

## Raw
- File XLSX: PenaleFlussi20142025.xlsx, sheet "Data"
- 17.653 righe raw, 17.652 righe clean (1 riga Totale scartata dal filtro Anno NOT NULL)
- 8 colonne: Ufficio, Sezione, Distretto, Circondario/Sede, Anno, Sopravvenuti, Definiti, Pendenti Finali
- Anno è stringa "2014" — cast_int in clean.sql lo converte

## V0: solo 2014-2025
- Il file storico (PenaleFlussi20052013.xlsx) ha struttura multi-sheet complessa:
  - Sheet "Dati nazionali" (6 colonne, no distretto)
  - Sheet "Dati distrettuali" (7 colonne, no sede/circondario)
  - Sheet per ufficio (Tribunale, Procura, ecc.) con 8 colonne
  - Sheet sorveglianza con struttura completamente diversa
- Per v0 copriamo solo 2014-2025. Lo storico richiede normalizzazione separata.

## Clean
- Clean.sql usa macro standard: cast_int, normalize_string
- Ufficio → tipo_ufficio, Circondario/Sede → sede

## Da fare
- [x] Run v0 su anno campione (2025) — 17.652 righe OK
- [ ] v1: unire PenaleFlussi20052013.xlsx (normalizzare 15+ sheet e colonne)
- [ ] Allineare schema a civile_flussi per join incrociato
- [ ] Notebook esplorativo
