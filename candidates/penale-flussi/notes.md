# Note tecniche — penale-flussi

## Raw
- File XLSX: PenaleFlussi20142025.xlsx, sheet "Data"
- 17.653 righe, 8 colonne
- Colonne: Ufficio, Sezione, Distretto, Circondario/Sede, Anno, Sopravvenuti, Definiti, Pendenti Finali
- Anno è stringa "2014" (non intero)

## V0: solo 2014-2025
- Il file storico (PenaleFlussi20052013.xlsx) ha struttura multi-sheet complessa:
  - Sheet "Dati nazionali" (6 colonne, no distretto)
  - Sheet "Dati distrettuali" (7 colonne, no sede/circondario)
  - Sheet per ufficio (Tribunale, Procura, ecc.) con 8 colonne
  - Sheet sorveglianza con struttura diversa
- Per v0 copriamo solo 2014-2025. Lo storico richiede lavoro di normalizzazione separato.

## Clean
- Clean.sql tipizza Anno come INTEGER, Sopravvenuti/Definiti/Pendenti come INTEGER
- Ufficio diventa tipo_ufficio, Circondario/Sede diventa sede

## Da fare
- [ ] v1: unire PenaleFlussi20052013.xlsx (normalizzare sheet e colonne)
- [ ] Allineare schema a civile_flussi per join
- [ ] Run v0 su anno campione
