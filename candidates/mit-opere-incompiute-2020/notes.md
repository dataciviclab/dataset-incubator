# Notes

## Tecnico

- CSV verificato con `UTF-8-BOM` e separatore `;`
- il file contiene una riga `TOT` e due righe vuote finali da ignorare
- `Codice_CUP` e la chiave naturale piu solida per dedup prudente
- `Localizzazione_codice_ISTAT` e quasi completo; `Localizzazione_codice_NUTS` molto meno affidabile

## Analitico

- il perimetro iniziale resta su uno snapshot al `31/12/2020`
- primo taglio consigliato: stato opera, avanzamento, cause, distribuzione territoriale di base
- il confronto con altre annualita va trattato come gate successivo, non come requisito iniziale

## Cautele

- il file nazionale e incompleto per design: non copre tutte le regioni
- confronti nazionali o pieni tra regioni non sono difendibili senza chiarire la copertura
- alcune opere risultano con avanzamento `100%` pur essendo classificate come incompiute: da trattare come segnale amministrativo, non errore automatico
