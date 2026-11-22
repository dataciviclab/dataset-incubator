# Notes

## Tecnico

- Il dataflow `DCSS_BULK_ABITAZIONI` e' marcato `NonProductionDataflow` e non entra nel
  catalogo SDMX standard (4.996 dataflow scansionati il 2026-11-22). Il raw va preso dal
  file in `ATTACHED_DATA_FILES`, con URL pinnato: se ISTAT cambia il path, il run fallisce
  in modo rumoroso invece di produrre un dataset vuoto.
- Stesso pattern `DWL/PERMPOP/...` della matrice pendolarismo (scouted, non ancora intaken).
- `clean.read.all_varchar: true` e' obbligatorio: `ITTER107` contiene codici con zeri
  iniziali (`001001`) che lo sniffing leggerebbe come interi, perdendo tre caratteri e
  rompendo il join con `comuni_master`.
- Il file ha BOM UTF-8 sul primo header: DuckDB lo assorbe, il nome colonna resta `ITTER107`.
- `warn_removed_columns: false` in `clean.validate.promotion`: il clean rinomina
  esplicitamente tutte le 21 colonne raw, quindi il monitor di transizione le segnalerebbe
  come rimosse a ogni run (rumore, non segnale).

## Analitico

- Le due edizioni non sono omogenee:
  - **2021** = enumerazione completa -> per comune: totale, occupate, non occupate.
  - **2019** = edizione campionaria -> per comune: occupate per titolo di possesso, con
    valori decimali (stime), **senza** il totale dello stock.
- Di conseguenza: il **tasso di sfitto esiste solo per il 2021**, e il confronto 2019/2021
  e' possibile solo sulle abitazioni occupate. I due mart sono tenuti separati per questo.
- "Non occupata" non significa "disponibile": dentro ci sono seconde case, immobili in
  ristrutturazione, case inagibili, abitazioni in territori senza domanda. Il dato misura
  lo stock non occupato, non l'offerta.
- La geografia dello sfitto (massimi in comuni alpini e localita' di villeggiatura) e' la
  prova che l'equazione casa vuota = casa disponibile e' falsa.

## Cautele

- Il 2019 e' campionario: i valori decimali non vanno presentati come conteggi.
- 16 comuni su 7.920 non hanno il dato 2021 (accorpamenti e variazioni amministrative).
- La mediana del tasso di sfitto cambia molto con la soglia dimensionale: 34,6% su tutti i
  comuni, 29,9% sui comuni con almeno 1.000 abitazioni. Va sempre dichiarata la popolazione
  di riferimento.
- Nessuna causalita': il tasso di sfitto non dice nulla, da solo, sui canoni o sul turismo.
  L'incrocio con OMI (canoni per zona) e con le locazioni brevi e' un lavoro successivo e
  richiede le serie storiche.
