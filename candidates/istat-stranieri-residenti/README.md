# istat-stranieri-residenti

**Stranieri residenti al 1 gennaio per provincia e cittadinanza (2019-2023)** — ISTAT `29_317_DF_DCIS_POPSTRCIT1_1` via **DBnomics**.

## Domanda civica

Dove vivono gli stranieri residenti in Italia, e di quale cittadinanza? Lo stock della popolazione straniera è il denominatore di tutto il resto (permessi, lavoro, scuola, cittadinanza acquisita): senza la sua geografia, ogni tasso resta nazionale.

La tensione: la popolazione straniera è **9,1% del totale** (dato Eurostat `MIGR_POP1CTZ` 2025 — questo candidate copre 2019-2023), ma è distribuita in modo molto disomogeneo tra province — e la sua composizione per cittadinanza cambia da territorio a territorio.

## Fonte

- **Ente**: ISTAT — dataflow `29_317` (sotto-dataset `DF_DCIS_POPSTRCIT1_1`, "Italy, regions, provinces - Country of citizenship")
- **Canale**: **DBnomics** (`type: dbnomics`, provider ISTAT) — mirror, nessun rate-limit SDMX
- **Copertura**: **2019-2023** · **134 territori** (Italia, 5 ripartizioni, 22 regioni, 106 province) · 212 cittadinanze (paesi + aree geopolitiche)
- **Misura**: stranieri residenti al 1 gennaio (`FJAN`)

## Perché vale la pena

- **Territorio**: Eurostat copre la popolazione straniera solo a livello **nazionale** (`MIGR_POP1CTZ`); ISTAT scende a **provincia**.
- **Cross-check con Eurostat**: IT 2023 = **5.141.341**, **identico** a `MIGR_POP1CTZ` 2023 → le due fonti concordano al numero.

## Output minimo atteso

- Clean parquet + mart `mart_stranieri_residenti` (anno × territorio × livello × cittadinanza)
- Numeri chiave 2023: Italia 5.141.341; top cittadinanze: Romania (1.081.836), Albania (416.829), Marocco (415.088), Cina (307.038), Ucraina (249.613); top province: Roma (511.332), Milano (475.171), Torino (214.860), Brescia (150.383), Firenze (128.290)

## Perimetro v0

- Tutti i livelli territoriali, marcati in `livello`; la colonna **`aggregato`** marca le righe che NON sono "foglie" (territorio macro o cittadinanza non-paese)
- **Ricetta per numeri corretti** (cubo multi-livello con aggregati sovrapposti):
  - **Totale nazionale**: `livello='nazionale' AND cittadinanza_codice='WORLD'`
  - **Dettaglio sommabile**: `livello='provincia' AND NOT aggregato` (provincia × paese)
  - ⚠️ **Non sommare senza entrambi i filtri**: `WHERE NOT aggregato` da solo somma regione **e** provincia (2×); `livello='nazionale'` da solo include `WORLD` **e** i paesi (2×)
- Sesso = totale (`SEX=9`)

## Criterio di promozione

- Estensione della serie storica (qui 2019-2023): verificare se una fonte complementare copre gli anni precedenti
- Join validato con un codelist territoriale condiviso

## Stato

`candidate` — run verificato: clean 104.619 righe, mart 104.619, **readiness 8/8**.

## Note tecniche

- **Gotcha `NA`**: la cittadinanza `NA` è **Namibia**, non un valore mancante. Pandas la legge come `NaN` per default — i codelist sono generati con `keep_default_na=False`. DuckDB (toolkit) la legge correttamente.
- La serie DBnomics di questo dataflow copre solo 2019-2023 (verificato anche sul parent `29_317`).
- `livello` derivato dalla lunghezza del codice ISTAT (euristica documentata).
