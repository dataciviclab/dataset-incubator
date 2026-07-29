# Elezioni Politiche 1948-2022 — risultati per comune

Risultati delle elezioni politiche (Camera dei Deputati e Senato della Repubblica) a livello comunale per tutte le 19 tornate dal 1948 al 2022.

**38 file ZIP** (19 Camera + 19 Senato) dall'Archivio storico elettorale del DAIT.

**Volume**: 3.78M righe, 21 colonne.

## Schema (21 colonne)

| Colonna | Tipo | Descrizione |
|---|---|---|
| `data_elezione` | DATE | Data del voto |
| `camera_senato` | VARCHAR | 'C' = Camera, 'S' = Senato |
| `circoscrizione` | VARCHAR | Circoscrizione elettorale |
| `provincia` | VARCHAR | Provincia (solo Camera proporzionale/Porcellum e Senato Porcellum) |
| `comune` | VARCHAR | Denominazione comune |
| `collegio_plurinominale` | VARCHAR | Collegio plurinominale |
| `collegio_uninominale` | VARCHAR | Collegio uninominale |
| `elettori_totali` | BIGINT | Elettori iscritti totali |
| `elettori_maschi` | BIGINT | Elettori maschi |
| `votanti_totali` | BIGINT | Votanti totali |
| `votanti_maschi` | BIGINT | Votanti maschi |
| `schede_biache` | BIGINT | Schede bianche |
| `lista` | VARCHAR | Lista o descrizione coalizione |
| `voti_lista` | BIGINT | Voti alla lista |
| `descr_lista` | VARCHAR | Descrizione estesa lista (solo Rosatellum) |
| `cognome` | VARCHAR | Cognome candidato uninominale |
| `nome` | VARCHAR | Nome candidato uninominale |
| `luogo_nascita` | VARCHAR | Luogo di nascita candidato |
| `data_nascita` | VARCHAR | Data di nascita candidato |
| `sesso` | VARCHAR | Sesso candidato ('M'/'F') |
| `voti_candidato` | BIGINT | Voti al candidato uninominale |

## Mart analitici

| Mart | Granularità | Righe | Cosa produce |
|---|---|---|---|
| `mart_voti_elezioni_politiche` | comune × lista × Camera/Senato × anno | 3.65M | Voti lista, affluenza%, % lista sul comune |
| `mart_candidati` | circoscrizione × Camera × anno | 7 epoche | Demografia candidati uninominali (1994-2001, 2018-2022) |
| `mart_trend` | circoscrizione × Camera × anno | 929 | Trend affluenza 1948-2022, CAGR, var. assoluta |

## Epoche elettorali

| Periodo | Sistema | Candidati uninominali | Collegi |
|---|---|---|---|
| 1948-1992 | Proporzionale puro | No | No |
| 1994-2001 | Mattarellum (misto) | Sì | Plurinominale + Uninominale |
| 2006-2013 | Porcellum (proporzionale con premio) | No | No |
| 2018-2022 | Rosatellum (misto) | Sì | Plurinominale + Uninominale |

## Dati salienti

- **Affluenza**: 92.8% (1953) → 62.8% (2022) — crollo di 30 punti percentuali in 74 anni
- **Calo più marcato**: Camera dal 92.4% (1948) al 63.8% (2022)
- **Candidati uninominali**: disponibili per Mattarellum (1994-2001, solo Camera) e Rosatellum (2018-2022, Camera+Senato)
- **Quote genere 2022**: Camera 41.4% donne, età media 50.2; Senato 40.9% donne, età media 56.8
- **Quote genere 1994**: Camera 0% donne (nessuna candidata uninominale registrata)

## Limiti noti

- `mart_candidati`: formato data_nascita variabile tra tornate. 1994 e 2001 funzionano (età disponibile). 1996 non ha data_nascita nei CSV storici (età N/D). 2018 Camera funziona (età 48.4), Senato 2018 no. 2022 funziona per entrambi.
- `mart_trend`: usa la media semplice dell'affluenza per circoscrizione (non pesata per elettori).

## Fonte

**Eligendo** — Archivio storico elettorale del DAIT (Ministero dell'Interno)
URL: https://elezionistorico.interno.gov.it/eligendo/opendata.php
Licenza: CC BY 4.0

## Issue

DataCivicLab/dataset-incubator#523

## Cross con altri dataset del Lab

| Dataset | Chiave | Domanda |
|---|---|---|
| `irpef_comunale` | comune | I comuni ricchi votano diversamente? |
| `dait_amministratori_locali` | comune | Il colore dell'amministrazione corrisponde al voto? |
| `popolazione_istat_comunale` | comune | L'astensione è correlata all'età della popolazione? |
| `ispra_ru_base` | comune | I comuni virtuosi nell'ambiente votano verde? |
| `consip_consumi_convenzione` | comune | La spesa pubblica correla col voto? |
