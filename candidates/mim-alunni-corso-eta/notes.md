# Notes

## Tecnico

- file v0 intake: `ALUCORSOETASTA20242520250831.csv`
- fonte CSV diretta su `catalogo/elements1/`
- `CODICESCUOLA` è presente e stabile per il join con il support dataset
- clean: 301.840 righe, perdita zero rispetto al raw
- **4 mart**: primaria, sec_I, sec_II, all (tutti per comune)
- I filtri per ordine stanno nel mart SQL, non nella clean

## Analitico

- framing ammesso: trend/pressione demografica scolastica per ordine
- framing escluso: sovraffollamento o alunni/classe
- Nota: sec_II ha meno righe (1391) perché ci sono meno comuni con scuole secondarie II grado

## Cautele

- nessuna inferenza diretta su classi o qualità dell'offerta scolastica
- sec_II min_rows abbassato a 1000 (dato reale: 1391 comuni)

## Log modifiche

- 2026-04-24 — aggiunte 3 nuove mart (secondaria I, II, all) + notebook v0 da template
