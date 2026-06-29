# Elezioni Regionali 2018-2024 — risultati per comune

Risultati delle elezioni regionali italiane a livello comunale, da Eligendo (DAIT).

## Dati

**Periodo**: 2018-2024 (6 anni, 9 tornate)
**Righe totali**: ~117.879
**Qualità clean**: 100/100

| Anno | Tornate | Regioni | Righe clean | Affluenza media |
|---|---|---|---|---|
| 2018 | 04/03 | Lombardia, Lazio | 35.060 | 71,9% |
| 2019 | 10/02, 24/03, 26/05, 27/10 | Abruzzo, Basilicata, Piemonte, Umbria | 24.645 | 61,2% |
| 2020 | 26/01 | Emilia-Romagna, Calabria | 10.299 | 53,7% |
| 2021 | 03/10 | Calabria | 8.484 | 43,5% |
| 2023 | 12/02 | Lombardia, Lazio | 24.125 | 42,9% |
| 2024 | 09/06 | Piemonte | 15.266 | 59,2% |

### Escluse
- 20/09/2020: file XLSX non gestiti dal toolkit

### Schema clean (12 colonne)

| Colonna | Tipo | Note |
|---|---|---|
| `data_elezione` | DATE | Data del voto |
| `regione` | VARCHAR | |
| `circoscrizione` | VARCHAR | |
| `provincia` | VARCHAR | |
| `comune` | VARCHAR | |
| `elettori` | BIGINT | |
| `votanti` | BIGINT | |
| `schede_bianche` | BIGINT | |
| `candidato` | VARCHAR | Cognome e nome candidato presidente |
| `voti_candidato` | BIGINT | Voti al candidato presidente |
| `lista` | VARCHAR | Lista di appoggio |
| `voti_lista` | BIGINT | Voti alla lista |

Dato normalize dal preprocess: nomi colonna unificati, encoding utf-8, numeri interi.

### Mart

- `mart_voti_lista_comune` — voti aggregati per lista × comune × elezione

## Cross con altri dataset del Lab

| Dataset | Chiave | Domanda |
|---|---|---|
| `bdap_lea` | regione | Spesa sanitaria e voto regionale |
| `irpef_comunale` | comune | Reddito e voto |
| `elezioni_politiche` (issue #523) | comune × anno | Correlazione voto politiche vs regionali |
| `popolazione_istat_comunale` | comune | Affluenza e demografia |

## Fonte

**Eligendo** — Archivio storico elettorale del DAIT (Ministero dell'Interno)
URL: https://elezionistorico.interno.gov.it/eligendo/opendata.php
Licenza: CC BY 4.0

## Issue

#588 — Intake eligendo: elezioni regionali 2018-2024
