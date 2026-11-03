# Notes — mase_consumi_petroliferi

## Fonte e accesso

Stessa fonte degli altri candidate MASE (SISEN, API CMIS senza autenticazione).

| Cartella | File | Copertura | N |
|---|---|---|---|
| `consumi_petroliferi/definitivi/` | `Consumi_Petroliferi_Definitivi_YYYY.xls(x)` | 2002-2025 (annuale) | 24 |
| `consumi_petroliferi/preconsuntivi/{anno}/` | `Consumi_Petrolio_YYYY_MM.xls` | 2022-2026 (mensile) | ~81 |

- ID 2025 definitivi: `0900fde8800e07e4`
- **v0 usa i definitivi**: un file = un anno completo (12 mesi), self-contained
- I preconsuntivi sono un'altra forma (mensile, con confronto anno precedente + YTD);
  cartelle `2020_old`, `2021_old` e anni normali 2022-2026

## Shape del file (verificato 2025)

Foglio `CONSUMI PETROLIFERI`, report a **blocchi affiancati**:

- I° SEMESTRE: colonne 0-12 (prodotto, dettaglio, GEN, FEB, GEN.FEB, MAR, GEN.MAR, …)
- II° SEMESTRE: colonne 13-26 (prodotto, dettaglio, LUG, GEN.LUG, AGO, GEN.AGO, …)
- righe 0-3 = titolo / anno / intestazioni / mesi → `read.skip=4`, `header: false`
- il nome prodotto (col0) è solo sulla prima riga del blocco; le righe successive
  hanno celle vuote o i marcatori `DI CUI:` / `=` → forward-fill che li ignora
- le colonne **cumulative** (`GEN.FEB`, `GEN.MAR`, …) vanno ignorate: si usano solo
  le colonne mese
- unità: **migliaia di tonnellate** (,000 tonn.)

## Tipi colonna — nota toolkit

Le colonne mese arrivano con **tipi misti** (VARCHAR/DOUBLE): basta una cella vuota o
una stringa perché DuckDB tipizzi `gen` come VARCHAR e `feb` come DOUBLE. `UNPIVOT`
richiede tipi uniformi e fallisce senza cast.

- `clean.read.all_varchar` **non si applica ai file Excel**: è gestito solo nel path CSV
  (`core/csv_read.py`). Il path Excel (`core/read_excel.py`) non lo legge → viene
  **ignorato silenziosamente**. Candidato a miglioramento del toolkit.
- `clean.read.columns` per Excel **rinomina** soltanto: il tipo dichiarato è ignorato
  (`read_excel.py` usa solo `parse_column_value(...)[0]`).
- Soluzione adottata: `SELECT COLUMNS(*)::VARCHAR` in una CTE di `clean.sql`. Una riga
  invece di 12 cast. E nessuna mapping `columns`: con `header: false` il reader nomina
  già `col0..colN`.

## Controlli di coerenza (2025)

- benzina = 8.937 kt, carboturbo = 5.081 kt → coincidono con i totali `GEN.DIC` del foglio
- 8 prodotti × 12 mesi = 96 righe; nessun null

## Insidie

- Il numero di colonne lette dipende dal foglio: se cambia, il riferimento posizionale
  `col2..col25` va rivisto → verificare `toolkit inspect` a ogni nuovo anno
- Le etichette prodotto hanno **doppie spaziature** (`AUTO  TOTALE`, `TOTALE  GASOLI`)
  → normalizzate con `regexp_replace(x, ' +', ' ', 'g')`
- Anche `LUBRIFICANTI TOTALE` è un prodotto senza dettaglio (come GPL, BITUMI)

## Multi-anno (next step)

Come per gli altri candidate MASE: un file per anno con ID non deterministico → serve
una `raw` di tipo `script` che enumera la cartella e scarica ogni file.

## Licenza

Non dichiarata sul portale MASE. Da chiarire prima della pubblicazione sull'Explorer.
