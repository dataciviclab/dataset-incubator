# Elezioni Regionali 2018-2024 — risultati per comune

Risultati delle elezioni regionali italiane a livello comunale.

## Dati

Periodo: 2018-2024 (in progress — attivo 2023)
Tornate: 9 totali, esclusa 2020-09-20 (file Excel)

### Schema clean

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

### Mart

- `mart_voti_lista_comune` — voti aggregati per lista × comune × elezione

## Cross con altri dataset

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

#588 — Intake eligendo: elezioni regionali
