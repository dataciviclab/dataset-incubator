# mur-contribuzione-universitaria

Candidate per il gettito della contribuzione studentesca MUR per ateneo e tipologia di gettito, con serie storica 2017-2024.

> **Nota scope**: pipeline multi-anno reale con `dataset.years` + source CKAN annuale. Il perimetro verificato e' 2017-2024; il claim 2009-2024 non e' supportato dal portale MUR con la stessa copertura/resource shape.

## Stato

`intake` — pipeline multi-anno raw → clean → mart verificata sul perimetro 2017-2024.

## Issue

- `dataciviclab/dataset-incubator#150`

## Domanda guida

Come varia nel tempo il gettito della contribuzione studentesca tra atenei e tipologia di voce (corsi di laurea, dottorato, master, tassa regionale DSU, esami di stato, ecc.)? Quali atenei generano il gettito piu alto per singola tipologia e quale peso ha ciascuna voce sul totale nei diversi anni disponibili?

## Fonte

- **MUR – Contribuzione e interventi atenei** (portale dati-ustat)
- URL base: https://dati-ustat.mur.gov.it
- Licenza: IODL-2.0 (Pubblico Dominio)
- Accesso: **DataStore API** (datastore_active=true) con paginazione automatica (toolkit v1.29.0+)
- Formato: CSV via DataStore (`,`, utf-8) o URL diretto (`;`, cp1252) — sniffing automatico
- Risorse annuali CKAN: `{year}-contribuzione-e-interventi-atenei` → `{year} Gettito della contribuzione studentesca`
- Perimetro verificato: 2017-2024
- Nota temporale: i file annuali 2017-2024 espongono nel campo `ANNO_SOLARE` la serie 2016-2023 (shift -1 anno)

## Output

- Mart annuale: `mart_gettito_ateneo_tipo` — gettito per ateneo e tipologia di gettito con colonna `anno`

## Perché vale la pena incubarlo

- Tema ad alta domanda civica: costo dell'università e accesso allo studio
- Dati amministrativi ufficiali, comparabili tra ~100 atenei
- Il gettito per tipologia di voce permette confronti trasversali tra atenei e tra voci di contribuzione
- Aggiornamento annuale, dataset stabile sul portale CKAN MUR

## Criterio di promozione

- Estensione eventuale oltre il perimetro 2017-2024 solo se MUR espone annualita' piu vecchie con risorse equivalenti o se si introduce una fonte alternativa affidabile
- Join con dataset iscritti per ateneo (disponibile come risorsa separata nello stesso portale MUR per calcolare quota esoneri/iscritti)

## Cautele

- **Shift temporale**: il file CKAN `{year}` contiene dati con ANNO_SOLARE = year-1; il mart riporta ANNO_SOLARE
- Il file gettito NON contiene il numero di iscritti — la quota esoneri/iscritti non è calcolabile da questo solo dataset
- DSU regionale e dati iscritti sono risorse separate nello stesso portale CKAN — fuori perimetro v0
- Granularità per ateneo, non per singolo corso di laurea
- Il portale MUR alterna formato CSV (`,`, utf-8 via DataStore vs `;`, cp1252 via URL diretto) — risolto con sniffing automatico + `normalize_duckdb_encoding` (toolkit v1.29.0)
- La risorsa del 2024 copre 100 atenei; 2017-2023 coprono 97-98 atenei (variazione annuale fisiologica)
