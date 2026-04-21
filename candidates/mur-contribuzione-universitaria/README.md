# mur-contribuzione-universitaria

Candidate per il gettito della contribuzione studentesca MUR per ateneo e tipologia di gettito, con serie storica attualmente implementata sugli anni 2017-2024.

> **Nota scope**: il candidate implementa una pipeline multi-anno reale nel toolkit (`dataset.years` + source CKAN annuale + `cross_year`). Il perimetro oggi verificato e' 2017-2024; il claim 2009-2024 non e' supportato dal portale MUR con la stessa copertura/resource shape.

## Stato

`intake` — pipeline multi-anno annuale raw -> clean -> mart + `cross_year` verificata sul perimetro 2017-2024.

## Issue

- `dataciviclab/dataset-incubator#150`

## Domanda guida

Come varia nel tempo il gettito della contribuzione studentesca tra atenei e tipologia di voce (corsi di laurea, dottorato, master, tassa regionale DSU, esami di stato, ecc.)? Quali atenei generano il gettito piu alto per singola tipologia e quale peso ha ciascuna voce sul totale nei diversi anni disponibili?

## Fonte

- **MUR – Contribuzione e interventi atenei** (portale dati-ustat)
- URL base: https://dati-ustat.mur.gov.it
- Licenza: IODL-2.0 (Pubblico Dominio)
- Formato: CSV, separatore `;`, encoding `cp1252`
- Risorse annuali CKAN: `{year}-contribuzione-e-interventi-atenei` -> `{year} Gettito della contribuzione studentesca`
- Perimetro verificato: 2017-2024
- Nota temporale: i file annuali 2017-2024 espongono nel campo `ANNO_SOLARE` la serie 2016-2023, che e' l'anno riportato nel mart

## Perché vale la pena incubarlo

- Tema ad alta domanda civica: costo dell'università e accesso allo studio
- Dati amministrativi ufficiali, comparabili tra ~100 atenei
- Il gettito per tipologia di voce permette confronti trasversali tra atenei e tra voci di contribuzione
- Aggiornamento annuale, formato CSV accessibile, naming annuale stabile sul portale CKAN MUR

## Output minimo atteso

- Mart annuale: `mart_gettito_ateneo_tipo` — gettito per ateneo e tipologia di gettito con colonna `anno`
- Cross-year: `mart_gettito_ateneo_tipo_multi_anno` — consolidato multi-anno dei mart annuali 2017-2024
- Notebook v0 di validazione

## Criterio di promozione

- Estensione eventuale oltre il perimetro 2017-2024 solo se MUR espone annualita' piu vecchie con risorse equivalenti o se si introduce una fonte alternativa affidabile
- Join con dataset iscritti per ateneo (disponibile come risorsa separata nello stesso portale MUR)
- denominatore per calcolare la quota esoneri / iscritti (non presente nel solo file gettito)

## Cautele

- Encoding `cp1252` (DuckDB non accetta `latin-1` come alias)
- Un file per anno — il candidate risolve il download via CKAN partendo dallo slug annuale del dataset e dal nome stabile della resource gettito
- Il perimetro dei file CKAN (`2017` ... `2024`) non coincide con il range del campo `anno` nel dato (`2016` ... `2023`)
- Dataset DSU regionale è su CKAN separato — fuori perimetro v0
- Il file gettito NON contiene il numero di iscritti: il denominatore per la quota esoneri non è in questo dataset
- Granularità per ateneo, non per singolo corso di laurea

## Prossimo passo

Valutare se il framing pubblico debba restare 2017-2024 o essere esteso con ulteriori fonti storiche che coprano le annualita' precedenti con contratto comparabile.
