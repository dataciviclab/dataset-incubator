# Notes — istat-trasporto-ferroviario

## Tecnico

- Fonte: ISTAT `117_1057` via **DBnomics** (`type: dbnomics`, provider ISTAT).
- Copertura 2004-2024; `years: [2026]` è l'anno di output.
- Clean: `anno`, `area`, `unita`, `merce_nst`, `unita_carico`, `paese_origine`, `paese_destinazione`, `categoria_trasporto`, `valore`.
- Il clean mantiene le dimensioni in chiaro; il mart seleziona quelle che contano.
- Mart `mart_ferrovia_intermodale`: filtra `unita = 'GC_TKM'` e usa `TOT_INTERMODAL` come numeratore e `ALL` come denominatore.

## Analitico

- `TOT_INTERMODAL` è il **subtotale pubblicato dalla fonte**: non va ricostruito sommando container, semi-rimorchi e casse mobili (sono sottoinsiemi non disgiunti).
- La quota è `tkm_intermodale / tkm_totali`, arrotondata a due decimali.

## Cautele

- Non sommare tra loro le tipologie di `unita_carico`.
- Molte dimensioni sono costanti per serie (`ALL`, `WORLD`): restano nel clean e non vanno lette come dettaglio.
- `unita` diversa da `GC_TKM` misura grandezze non confrontabili (tonnellate, viaggi): non aggregare unità diverse.
- L'eventuale dettaglio per `area` va verificato prima di sommare: il mart aggrega per anno.
