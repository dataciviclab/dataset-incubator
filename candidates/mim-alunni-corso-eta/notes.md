# Notes

## Tecnico

- file v0 intake: `ALUCORSOETASTA20242520250831.csv`
- fonte CSV diretta su `catalogo/elements1/`
- `CODICESCUOLA` è presente e stabile abbastanza per il join con il support dataset
- il candidate usa `support:` verso `mim-anagrafica-scuole-statali`
- il v0 resta single-year per evitare subito il blocker del naming scolastico multi-anno MIM

## Analitico

- framing ammesso: trend/pressione demografica scolastica
- framing escluso: sovraffollamento o alunni/classe
- focus iniziale sulle primarie per tenere la domanda più stretta e leggibile

## Cautele

- nessuna inferenza diretta su classi o qualità dell'offerta scolastica
- il mart v0 serve a verificare la tenuta del join geografico prima dell'estensione storica
