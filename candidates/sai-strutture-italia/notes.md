## Tecnico

- File unico CSV multi-anno (2018-2024)
- 46.299 righe, 26 colonne clean
- Encoding: UTF-8, delim: virgola
- Quote/escape configurati

## Analitico

- 83% delle strutture sono APPARTAMENTO (capienza media ~6 posti)
- Capienza/presenze solo per ultima rilevazione di ogni struttura

## Cautele

- Capienza e presenze sono **NULL per interi anni** (2018, 2019, 2021): in quegli
  anni è valido solo il conteggio delle strutture. Il mart non filtra su
  `capienza` (altrimenti perderebbe quegli anni) — `SUM` ignora i NULL.
- `sai_struttura_id` è univoco per rilevazione annuale, non nel file intero
  (9.907 strutture ricorrono in più anni).
- `data_fine` è VARCHAR (valori vuoti)
