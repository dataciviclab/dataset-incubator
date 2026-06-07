# Notes - mur-contribuzione-universitaria

## Stato

- intake iniziato 2026-04-21
- pipeline raw -> clean -> mart verificata (2017-2024)
- cross_year rimosso (debito tecnico: non risolveva shift temporale ANNO_SOLARE vs anno CKAN)
- issue: `dataciviclab/dataset-incubator#150`
- review: Matteo segnala disallineamento scope/domanda guida vs dato reale
- verifica CKAN MUR: per il gettito la shape annuale omogenea e' disponibile almeno per il periodo 2017-2024

## Fonte verificata

- Portale CKAN: `https://dati-ustat.mur.gov.it/api/3/action`
- **Risorse CSV con datastore_active=true** — il connector preferisce DataStore API
- Formato DataStore (2024): CSV, separatore `,`, encoding **utf-8**, 7 colonne (con `_id`)
- Formato URL diretto (2023): CSV, separatore `;`, encoding **cp1252**, 6 colonne (senza `_id`)
- Colonne: `_id` (solo datastore), ANNO_SOLARE, COD_Ateneo, NOME_ATENEO, CODICE_GETTITO, DESCRIZIONE_GETTITO, CONTO_ECONOMICO
- Contenuto: ~1.100 righe (100 atenei × 11 tipologie di gettito), A.A. 2023/24
- Slug annuali verificati con risorsa gettito coerente: `2017` ... `2024`
- Verifica output: i file CKAN 2017-2024 generano `ANNO_SOLARE` nel range 2016-2023
- Nota: 2024 resource ha 100 atenei; 2017-2023 hanno 97-98 atenei (variazione annuale)
- Nota shift temporale: il file CKAN `{year}` contiene dati con ANNO_SOLARE = year-1 (es. 2024 → 2023)

## Tech

- **Datastore API**: paginata con page_size=32000, loop offset (toolkit v1.29.0+)
- **Sniffing automatico**: `source: auto` + suggested_read.yml — non ci sono delim/encoding fissi
- **CONTO_ECONOMICO**: portale alterna formato double (datastore) e stringa con virgola decimale (URL diretto). Gestito con `cast(replace(cast(CONTO_ECONOMICO as varchar), ',', '.') as double)`
- **Encoding sniffato latin-1**: normalizzato a CP1252 via `normalize_duckdb_encoding` (toolkit v1.29.0+)
- **Line terminators**: CRLF

## Debug history

| Data | Problema | Fix |
|---|---|---|
| 2026-06-07 | clean.sql colonne non trovate (delim/encoding fissi sbagliati) | Rimossi delim/encoding da dataset.yml, sniffing automatico |
| 2026-06-07 | CONTO_ECONOMICO formato misto (double vs stringa) | `cast(varchar)` + replace in clean.sql |
| 2026-06-07 | DuckDB rifiuta latin-1 per file cp1252 | `normalize_duckdb_encoding()` (toolkit#346) |
| 2026-06-07 | Solo 10 atenei (100 righe) per datastore senza paginazione | Paginazione `_datastore_search()` (toolkit#347) |
| 2026-06-07 | cross_year non allineato (shift anno) | Rimosso cross_year |

## Cautele

- La copertura omogenea verificata e' 2017-2024; annualita' precedenti non risultano tutte disponibili con la stessa resource shape
- Il file gettito NON contiene il numero di iscritti — la quota esoneri/iscritti non è calcolabile da questo solo dataset
- DSU regionale è su CKAN separato — fuori perimetro v0
- Granularità solo ateneo, non per singolo corso di laurea
- Shift temporale: il file CKAN {year} contiene ANNO_SOLARE = year-1; il mart riporta ANNO_SOLARE (non l'anno CKAN)
