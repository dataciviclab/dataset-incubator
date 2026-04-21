# Notes - mur-contribuzione-universitaria

## Stato

- intake iniziato 2026-04-21
- issue: `dataciviclab/dataset-incubator#150`

## Fonte verificata

- URL: `https://dati-ustat.mur.gov.it/dataset/2024-contribuzione-e-interventi-atenei/resource/f3619f14-2e4a-4595-bc69-508b51ce79f8/download`
- Formato: CSV, semicolon-separated, encoding latin-1
- Colonne: ANNO_SOLARE, COD_Ateneo, NOME_ATENEO, CODICE_GETTITO, DESCRIZIONE_GETTITO, CONTO_ECONOMICO
- Primo anno disponibile nel file: 2023 (A.A. 2023/24)

## Tech

- Encoding: **cp1252** (NON latin-1) — DuckDB 1.5.1 non accetta 'latin-1' come alias, solo 'cp1252'
- Delimiter: `;` (non `,`)
- Decimali: virgola (`,`) nel campo CONTO_ECONOMICO → gestiti nella clean.sql con `replace(..., ',', '.')`
- Line terminators: CRLF (funziona con cp1252)

## Cautele

- Serie storica multi-anno non ancora verificata (2009-2023)
- Il file 2024 contiene solo A.A. 2023/24
- DSU regionale è su CKAN separato — fuori perimetro v0
- Granularità solo ateneo, non per singolo corso