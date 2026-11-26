# Notes — istat-migrazioni

## Tecnico

- Fonte: ISTAT `28_185_DF_DCIS_MIGRAZIONI_4` via **DBnomics** (`type: dbnomics`, provider ISTAT).
- Copertura: 2002-2024; `years: [2026]` è l'anno di output, il dato è storico.
- Clean: `anno`, `territorio_codice`, `territorio`, `livello`, `aggregato`, `immigrazioni`.
- `CHANGE_OF_RESIDENCE=FREIGN` restringe alle iscrizioni **dall'estero**: con `ALL` il flusso include anche le migrazioni interne.
- `livello` è derivato dalla lunghezza del codice ISTAT (euristica); `aggregato` marca le righe non-foglia.
- Mart: `mart_migrazioni` (anno × regione, quota % sull'Italia) e `mart_migrazioni_serie` (Italia per anno).

## Analitico

- Totale nazionale: `livello='nazionale' AND territorio_codice='IT'`.
- Dettaglio sommabile: `livello='regione' AND NOT aggregato`.

## Cautele

- **Non sommare i livelli**: `WHERE NOT aggregato` da solo somma regione **e** provincia (2×).
- **Il livello provincia è parziale**: per una sommatoria completa usare `livello='regione'`.
- Cross-check con Eurostat `MIGR_IMM1CTZ`: allineato 2019-2023; il 2024 diverge (revisione) e va chiarito in promozione.
- Cittadinanza, età e sesso non sono disponibili a livello provinciale in questo dataflow.
