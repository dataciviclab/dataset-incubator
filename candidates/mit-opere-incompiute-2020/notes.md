# Notes

## Tecnico

- CSV verificato con `UTF-8-BOM` e separatore `;`
- il file contiene una riga `TOT` e due righe vuote finali da ignorare
- **Riga TOT**: è un aggregato editoriale calcolato dal MIT (totale nazionale), non un'opera reale — filtro `codice_cup <> 'TOT'` nel clean è giustificato
- `Codice_CUP` è la chiave naturale più solida per dedup prudente
- **Dedup**: il file sorgente MIT contiene 3 duplicati su `codice_CUP` (stessa opera ripetuta con dati identici) — il clean li rimuove mantenendo la prima occorrenza in ordine alfabetico per `titolo_opera_incompiuta`, `stazione_appaltante`
- `Localizzazione_codice_ISTAT` e quasi completo; `Localizzazione_codice_NUTS` molto meno affidabile

## Analitico

- il perimetro iniziale resta su uno snapshot al `31/12/2020`
- primo taglio consigliato: stato opera, avanzamento, cause, distribuzione territoriale di base
- il confronto con altre annualita va trattato come gate successivo, non come requisito iniziale

## Cautele

- il file nazionale e incompleto per design: non copre tutte le regioni
- confronti nazionali o pieni tra regioni non sono difendibili senza chiarire la copertura
- alcune opere risultano con avanzamento `100%` pur essendo classificate come incompiute: da trattare come segnale amministrativo, non errore automatico
