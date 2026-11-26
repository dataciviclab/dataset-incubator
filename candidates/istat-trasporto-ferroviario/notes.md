# Notes — istat-trasporto-ferroviario

## Tecnico

- Fonte: ISTAT `117_1057` via **DBnomics** (`type: dbnomics`, provider ISTAT).
- Copertura 2004-2024; `years: [2026]` è l'anno di output.
- Clean: `anno`, `area`, `unita`, `merce_nst`, `unita_carico`, `paese_origine`, `paese_destinazione`, `categoria_trasporto`, `valore`.
- Il clean mantiene le dimensioni in chiaro; il mart seleziona quelle che contano.
- Mart `mart_ferrovia_intermodale`: filtra `unita = 'GC_TKM'`, `merce_nst = 'ALL'`, `paese_origine = 'WORLD'`, `paese_destinazione = 'WORLD'`, `categoria_trasporto = 'ALL'`; usa `TOT_INTERMODAL` come numeratore e `ALL` come denominatore.

## Analitico

- In `GC_TKM` le componenti sommano esattamente a `TOT_INTERMODAL` (2009-2024). Il rischio è nei **subtotali di dimensione**: senza i filtri `ALL`/`WORLD` il mart duplica le righe (2024: 137,8 M tkm contro 48,3 M).
- La quota è `tkm_intermodale / tkm_totali`, arrotondata a due decimali.
- `TOT_INTERMODAL` esiste dal 2009: 2004-2008 hanno quota `NULL`.

## Cautele

- Non sommare tra loro le tipologie di `unita_carico`.
- Molte dimensioni sono costanti per serie (`ALL`, `WORLD`): restano nel clean e non vanno lette come dettaglio.
- `unita` diversa da `GC_TKM` misura grandezze non confrontabili (tonnellate, viaggi): non aggregare unità diverse.
- L'eventuale dettaglio per `area` va verificato prima di sommare: il mart aggrega per anno.
