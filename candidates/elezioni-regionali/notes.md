# Note tecniche — elezioni_regionali

## Perimetro

Attuale: 2023 (Lazio, Lombardia — 12/02/2023)
Prossimi: 2024 (Piemonte), 2021, 2020, 2019 (×4), 2018

## Variazioni schema tra anni

| Anno | File | Delim | Numeri | Colonne particolari |
|---|---|---|---|---|
| 2023 | catalogoagid CSV diretto | `;` | interi | `ELETTORITOT, VOTICAND, DESCRLISTA` |
| 2024 | ZIP → 1 CSV combinato | `;` | interi | `REG, CIRC, PROV, ALTRONOME, VOTICANDIDATO` |
| 2021 | ZIP → 2 TXT (scrutini+pref) | `;` | comma decimal | `provincia` lowercase, `ALTRO_NOME` |
| 2020-gen | ZIP → 2 TXT | `;` | comma decimal | Stesso schema 2018 |
| 2020-set | ZIP → XLSX | — | — | Da escludere (Excel) |
| 2019 (×4) | ZIP → 2 TXT | `;` | comma decimal | Stesso schema 2018 |
| 2018 | ZIP → 2 TXT | `;` | comma decimal | Schema base |

## Comma decimal

2018-2021 usano la virgola come separatore decimale (es. `5849,00`).
DuckDB li legge come VARCHAR. Nel clean.sql: `TRY_CAST(REPLACE(colonna, ',', '.') AS DOUBLE)` oppure `TRY_CAST(colonna AS BIGINT)` per valori interi con `,00`.

Preferisco `TRY_CAST(REPLACE(colonna, ',', '') AS BIGINT)` che elimina la virgola e tratta come intero.

## Preferenze

Le preferenze dei consiglieri sono in un secondo file dentro ogni ZIP (nome variabile).
Non incluse nel perimetro iniziale. Mart futuro.

## Date elezione

Le date non sono nei CSV — vanno derivate dal nome file ZIP. Nel clean.sql vanno hardcoded o passate come parametro.

## 2020-09-20 (escluso)

File XLSX per scrutini. Il toolkit non supporta Excel.
Soluzione futura: estrarre XLSX a mano e convertire in CSV, oppure estendere toolkit.

## Nomi file dentro ZIP

- 2018-2020, 2023: `regionali-YYYYMMDD.txt` / `.csv`
- 2021: `scrutini-YYYYMMDD.txt`
- 2024: `regionali-YYYYMMDD.csv` (unico file)
