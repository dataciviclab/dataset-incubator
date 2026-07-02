## Tecnico

- File unico CSV multi-anno (2018-2024)
- 46.299 righe, 26 colonne clean
- Encoding: UTF-8, delim: virgola
- Quote/escape configurati

## Analitico

- 83% delle strutture sono APPARTAMENTO (capienza media ~6 posti)
- Capienza/presenze solo per ultima rilevazione di ogni struttura

## Cautele

- Capienza zero per rilevazioni storiche (pre-2020)
- `sai_struttura_id` non univoco: più rilevazioni per stessa struttura
- `data_fine` è VARCHAR (valori vuoti)
