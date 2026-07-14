# Elezioni Politiche 1948-2022 — risultati per comune

Risultati delle elezioni politiche (Camera dei Deputati e Senato della Repubblica) a livello comunale per tutte le 19 tornate dal 1948 al 2022.

**38 file ZIP** (19 Camera + 19 Senato) dall'Archivio storico elettorale del DAIT.

## Schema unificato

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
| `lista` | VARCHAR | Lista o desrizione coalizione |
| `voti_lista` | BIGINT | Voti alla lista |
| `desr_lista` | VARCHAR | Desrizione estesa lista (solo Rosatellum) |
| `onome` | VARCHAR | Cognome candidato uninominale |
| `nome` | VARCHAR | Nome candidato uninominale |
| `luogo_nascita` | VARCHAR | Luogo di nascita candidato |
| `data_nascita` | DATE | Data di nascita candidato |
| `sesso` | VARCHAR | Sesso candidato ('M'/'F') |
| `voti_andidato` | BIGINT | Voti al candidato uninominale |

## Epoche elettorali

| Periodo | Sistema | Candidati uninominali | Collegi |
|---|---|---|---|
| 1948-1992 | Proporzionale puro | No | No |
| 1994-2001 | Mattarellum (misto) | Si | Plurinominale + Uninominale |
| 2006-2013 | Porcellum (proporzionale con premio) | No | No |
| 2018-2022 | Rosatellum (misto) | Si | Plurinominale + Uninominale |

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
