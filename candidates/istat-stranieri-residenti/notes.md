# Notes — istat-stranieri-residenti

## Tecnico

- Fonte: ISTAT `29_317_DF_DCIS_POPSTRCIT1_1` via **DBnomics** (`type: dbnomics`, provider ISTAT).
- Copertura: 2019-2023; misura `FJAN` = stranieri residenti al 1° gennaio.
- Clean: `anno`, `territorio_codice`, `territorio`, `livello`, `cittadinanza_codice`, `cittadinanza`, `aggregato`, `residenti`.
- **Gotcha `NA`**: la cittadinanza `NA` è **Namibia**, non un valore mancante. I codelist sono generati con `keep_default_na=False`; DuckDB la legge correttamente.
- Mart: `mart_stranieri_residenti` (anno × regione × cittadinanza, quota %) e `mart_stranieri_residenti_serie` (Italia per anno).

## Analitico

- Totale nazionale: `livello='nazionale' AND cittadinanza_codice='WORLD'`.
- Dettaglio sommabile: `livello='regione' AND NOT aggregato`.

## Cautele

- **Cubo multi-livello**: non sommare i livelli; `NOT aggregato` da solo somma regione **e** provincia (2×).
- **Provincia parziale**: per totali usare `livello='regione'`.
- Residuo apolidi `999`: la somma a regione è leggermente inferiore al totale `WORLD`; l'apolidia è a volte inclusa in `X777`.
- La serie DBnomics di questo dataflow copre solo 2019-2023 (verificato anche sul parent `29_317`).
- Sesso = totale (`SEX=9`).
