# Notes — istat-permessi

## Tecnico

- Fonte: ISTAT `29_348_DF_DCIS_PERMSOGG1_5` via **DBnomics** (`type: dbnomics`, provider ISTAT).
- Copertura: 2008-2024; misura `RESPER` = permessi di soggiorno validi al 1° gennaio (stock).
- Clean: `anno`, `territorio_codice`, `territorio`, `livello`, `cittadinanza_codice`, `cittadinanza`, `aggregato`, `permessi`.
- Il sotto-dataset `..._12` (motivo del permesso per provincia) non è pubblicato su DBnomics: il motivo non è in v0.
- `MARITAL_STATUS=99` è l'unico valore presente (totale), quindi il filtro non perde informazione.
- Mart: `mart_permessi` (anno × regione × cittadinanza, quota % sul totale regionale) e `mart_permessi_serie` (Italia per anno).

## Analitico

- Totale nazionale: `livello='nazionale' AND cittadinanza_codice='WORLD'`.
- Dettaglio sommabile: `livello='regione' AND NOT aggregato`.

## Cautele

- **Cubo multi-livello**: `livello='nazionale'` da solo include `WORLD` **e** i singoli paesi (2×); `NOT aggregato` da solo somma regione **e** provincia (2×).
- **Provincia parziale**: per totali usare `livello='regione'`.
- Residuo noto: gli apolidi `999` sono conteggiati anche in `X777`; la somma delle foglie supera `WORLD` di poche centinaia di unità.
- Cross-check con Eurostat `MIGR_RESVALID`: allineato 2020-2021, divergenze nei più recenti (revisioni/definizioni).
