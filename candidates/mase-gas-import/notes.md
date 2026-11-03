# Notes — mase_gas_import

## Fonte e accesso

- Portale: https://sisen.mase.gov.it/dgsaie/bilancio-gas-naturale (SPA React, i dati non sono nell'HTML)
- API CMIS, **nessuna autenticazione**:
  - lista cartelle: `GET /dgsaie/api/v1/cmis/folders?folder={path}`
  - lista documenti: `GET /dgsaie/api/v1/cmis/documents?folder={path}` (param `folder` = **path**, non ID)
  - download: `GET /dgsaie/api/v1/cmis/documents/{id}`
- Cartelle gas: `importazioni/`, `consumi/regionali/`, `consumi/provinciali/`, `bilancio/{anno}/`

## Shape del file (verificato)

`ImportazioniGasMensiliPerPaeseDiOrigine_2024.xlsx`, foglio `Foglio2`:

| Riga/col | Contenuto |
|---|---|
| A3 | titolo (dichiara l'anno) |
| B4 | "MESE" |
| riga 5 | nomi mesi (Gennaio…Dicembre) + `Totale` + `Peso %` |
| riga 6+ | paese in colonna A, valori mensili in M Sm³ |
| ultima riga | `Totale complessivo` (esclusa nel clean) |

- `read.skip=4` + `header=true` → header = riga 5; colonna 0 = paese (rinominata `paese`)
- `Foglio1` è un pivot ausiliario con dati sparsi: ignorato via `sheet_name: Foglio2`
- Le colonne mese arrivano con **tipi misti** (VARCHAR/DOUBLE) → cast a VARCHAR prima di `UNPIVOT`

## Run v0 (2024)

`toolkit run -c candidates/mase-gas-import/dataset.yml --year 2024` → **passed**, `readiness: ready (8/8)`.

- raw: 27 righe × 15 col (foglio `Foglio2`)
- clean: **265 righe × 4 col**
- mart: **265 righe**, 23 paesi, totale 2024 = **59.304 M Sm³** (coincide col "Totale complessivo" del file)
- controllo: `SUM(quota_pct)` = 100,0 per ogni mese; i totali mensili coincidono col file

**Warning attesi (non blocker)**:
- `transition:clean` segnala `-881,5% righe` e 11 colonne rimosse: è l'effetto dell'`UNPIVOT`
  (27 righe × 12 mesi → 265) e della selezione di 4 colonne su 15. Non è una perdita di dati.

## Insidie

- L'header del file 2024 dichiara `Totale 2022` → **bug di template MASE**, i valori sono 2024
- `ImportazioniGasMensiliPerPuntoIngresso` **manca il 2012**; il 2022 ha `_rev1` (usare la rev)
- Formati misti: `.xls` (2002-2019) vs `.xlsx` (2014+) → due engine (xlrd/openpyxl)
- Valori `0` legittimi (paesi senza import in un mese): non sono null

## Multi-anno (next step)

La fonte espone **un documento per anno**, con ID non deterministico. Il v0 usa l'ID del 2024.
Per il multi-anno serve una `raw` di tipo `script` che:
1. chiama `GET /cmis/documents?folder=/sg_dgsaie/gas_naturale/importazioni`
2. filtra i file `ImportazioniGasMensiliPerPaeseDiOrigine_YYYY` (preferendo `_rev1`)
3. scarica ogni file via `GET /cmis/documents/{id}`

Il layout `.xls` pre-2014 va verificato: `skip`/`sheet_name` possono differire.

## Piste collegate

- `consumi/regionali/` (2002+) e `consumi/provinciali/` (2004+) → candidate separato
  (`mase-gas-consumi-territoriali`), incrociabile con `comuni_master`
- `importazioni/` **per punto di ingresso** → secondo asse dello stesso tema
- Flussi giornalieri ENTSOG (Snam Rete Gas `IT-TSO-0001`, 2021+) → support, ma licenza ambigua
  (T&C Rev 3 vs pagina corporate ENTSOG)

## Licenza

Non dichiarata sul portale MASE. Da chiarire prima di pubblicare il dataset sull'Explorer.
Il dataset gemello `mase-prezzi-carburanti-mensili` usa la stessa fonte `mase_dgsaie`.
