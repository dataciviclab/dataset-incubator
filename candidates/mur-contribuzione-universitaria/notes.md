# Notes - mur-contribuzione-universitaria

## Stato

- intake iniziato 2026-04-21
- pipeline raw -> clean -> mart verificata
- cross_year verificato sul consolidato 2017-2024
- issue: `dataciviclab/dataset-incubator#150`
- review: Matteo segnala disallineamento scope/domanda guida vs dato reale
- verifica CKAN MUR: per il gettito la shape annuale omogenea e' disponibile almeno per il periodo 2017-2024

## Fonte verificata

- Portale CKAN: `https://dati-ustat.mur.gov.it/api/3/action`
- Formato: CSV, separatore `;`, encoding **cp1252**
- Colonne: ANNO_SOLARE, COD_Ateneo, NOME_ATENEO, CODICE_GETTITO, DESCRIZIONE_GETTITO, CONTO_ECONOMICO
- Contenuto: 1100 righe (100 atenei × 11 tipologie di gettito), A.A. 2023/24
- Slug annuali verificati con risorsa gettito coerente: `2017` ... `2024`
- Verifica output: i file CKAN 2017-2024 generano `ANNO_SOLARE` nel range 2016-2023
- Consolidato cross_year verificato: 8624 righe, `anno` 2016-2023

## Tech

- Encoding: **cp1252** — DuckDB 1.5.1 non accetta `latin-1` come alias, solo `cp1252`
- Delimiter: `;`
- Decimali: virgola (`,`) nel campo CONTO_ECONOMICO → gestiti in clean.sql con `replace(..., ',', '.')`
- Line terminators: CRLF

## Cautele

- La copertura omogenea verificata e' 2017-2024; annualita' precedenti non risultano tutte disponibili con la stessa resource shape
- Il file gettito NON contiene il numero di iscritti — la quota esoneri/iscritti non è calcolabile da questo solo dataset
- DSU regionale è su CKAN separato — fuori perimetro v0
- Granularità solo ateneo, non per singolo corso di laurea
