# elezioni-politiche — Note tecniche

## Issue
DataCivicLab/dataset-incubator#523

## Approccio
Script source (preprocess.py) invece di per-source http_file.

Motivo: 38 sorgenti ZIP con estrazione e unificazione necessaria.
Il toolkit processa solo la sorgente primary attraverso clean → mart.
Con http_file per-source, solo 1 ZIP verrebbe estratto.

preprocess.py scarica tutti i 38 ZIP, estrae i CSV/TXT e produce
un CSV unico con schema unificato.

## Fonte
Eligendo — Archivio storico elettorale DAIT (Ministero dell'Interno)
https://elezionistorico.interno.gov.it/eligendo/opendata.php

## URL pattern ZIP
Camera:  https://dait.interno.gov.it/documenti/opendata/camera/camera-{YYYYMMDD}.zip
Senato: https://dait.interno.gov.it/documenti/opendata/senato/senato-{YYYYMMDD}.zip

## 19 tornate (38 ZIP)
| Anno | Data | Sistema | File interno Camera | File interno Senato |
|------|------|---------|--------------------|--------------------|
| 1948 | 18-04 | Proporzionale | camera-19480418.txt | senato-19480418.txt |
| 1953 | 07-06 | Proporzionale | camera-19530607.txt | senato-19530607.txt |
| 1958 | 25-05 | Proporzionale | camera-19580525.txt | senato-19580525.txt |
| 1963 | 28-04 | Proporzionale | camera-19630428.txt | senato-19630428.txt |
| 1968 | 19-05 | Proporzionale | camera-19680519.txt | senato-19680519.txt |
| 1972 | 07-05 | Proporzionale | camera-19720507.txt | senato-19720507.txt |
| 1976 | 20-06 | Proporzionale | camera-19760620.txt | senato-19760620.txt |
| 1979 | 03-06 | Proporzionale | camera-19790603.txt | senato-19790603.txt |
| 1983 | 26-06 | Proporzionale | camera-19830626.txt | senato-19830626.txt |
| 1987 | 14-06 | Proporzionale | camera-19870614.txt | senato-19870614.txt |
| 1992 | 05-04 | Proporzionale | camera-19920405.txt | senato-19920405.txt |
| 1994 | 27-03 | Mattarellum | camera-19940327_Proporzionale.txt + Camera_19940327_Uninom_Cand&Contr.txt + Camera_19940327_Uninom_Scrutini.txt | senato-19940327.txt |
| 1996 | 21-04 | Mattarellum | camera-19960421_Proporzionale.txt + Camera_19960421_Uninom_Cand&Contr.txt + Camera_19960421_Uninom_Scrutini.txt | senato-19960421.txt |
| 2001 | 13-05 | Mattarellum | camera-20010513_Proporzionale.txt + Camera_20010513_Uninom_Cand&Contr.txt + Camera_20010513_Uninom_Scrutini.txt | senato-20010513.txt |
| 2006 | 09-04 | Porcellum | camera_italia-20060409.txt | senato_italia-20060409.txt |
| 2008 | 13-04 | Porcellum | camera_italia-20080413.txt | senato_italia-20080413.txt |
| 2013 | 24-02 | Porcellum | camera_italia-20130224.txt | senato_italia-20130224.txt |
| 2018 | 04-03 | Rosatellum | Camera2018_livComune.txt | Senato2018_livComune.txt |
| 2022 | 25-09 | Rosatellum | camera2022_Italia_LivComune.csv | Senato_Italia_LivComune.csv |

## Schemi verificati (file interni ZIP)

### Camera — Epoca 1 (1948-1992)
`camera-YYYYMMDD.txt` — 10 colonne:
CIRCOSCRIZIONE; PROVINCIA; COMUNE; ELETTORI; ELETTORI_MASCHI; VOTANTI; VOTANTI_MASCHI; SCHEDE_BIANCHE; LISTA; VOTI_LISTA

### Camera — Epoca 2 Mattarellum (1994-2001)
Proporzionale `camera-YYYYMMDD_Proporzionale.txt` — 10 colonne:
CIRCOSCRIZIONE; COLLEGIO; COMUNE; ELETTORI; ELETTORI_MASCHI; VOTANTI; VOTANTI_MASCHI; SCHEDE_BIANCHE; LISTA; VOTI_LISTA

Uninom candidati `Camera_YYYYMMDD_Uninom_Cand&Contr.txt` — 10 colonne:
circ; coll; comune; cognome; nome; datanascita; luogonascita; sesso; TOTVOTI; descrcontrass

### Camera — Epoca 3 Porcellum (2006-2013)
`camera_italia-YYYYMMDD.txt` — stesse 10 colonne epoca 1

### Camera — Epoca 4 Rosatellum (2018)
`Camera2018_livComune.txt` — 17 colonne:
CIRCOSCRIZIONE; COLLEGIOPLURINOMINALE; COLLEGIOUNINOMINALE; COMUNE; ELETTORI; ELETTORI_MASCHI; VOTANTI; VOTANTI_MASCHI; SCHEDE_BIANCHE; COGNOME; NOME; DATA_NASCITA; LUOGO_NASCITA; SESSO; VOTI_CANDIDATO; LISTA; VOTI_LISTA

### Camera — Epoca 5 Rosatellum (2022)
`camera2022_Italia_LivComune.csv` — 19 colonne:
DATAELEZIONE; CODTIPOELEZIONE; CIRC-REG; COLLPLURI; COLLUNINOM; COMUNE; ELETTORITOT; ELETTORIM; VOTANTITOT; VOTANTIM; SKBIANCHE; VOTILISTA; DESCRLISTA; COGNOME; NOME; LUOGONASCITA; DATANASCITA; SESSO; VOTICANDIDATO

### Senato — Epoca 1 (1948-1992)
`senato-YYYYMMDD.txt` — 10 colonne:
REGIONE; COLLEGIO; COMUNE; ELETTORI; ELETTORI_MASCHI; VOTANTI; VOTANTI_MASCHI; SCHEDE_BIANCHE; LISTA; VOTI_LISTA

### Senato — Epoca 2 (1994-2001)
`senato-YYYYMMDD.txt` — 10 colonne (stessa struttura epoca 1)

### Senato — Epoca 3 Porcellum (2006-2013)
`senato_italia-YYYYMMDD.txt` — 10 colonne:
REGIONE; PROVINCIA; COMUNE; ELETTORI_TOTALI; ELETTORI_MASCHI; VOTANTI_TOTALI; VOTANTI_MASCHI; SCHEDE_BIANCHE; LISTA; VOTI_LISTA

### Senato — Epoca 4 Rosatellum (2018)
`Senato2018_livComune.txt` — 17 colonne:
REGIONE; COLLEGIOPLURINOMINALE; COLLEGIOUNINOMINALE; COMUNE; ELETTORI; ELETTORI_MASCHI; VOTANTI; VOTANTI_MASCHI; SCHEDE_BIANCHE; COGNOME; NOME; DATA_NASCITA; LUOGO_NASCITA; SESSO; VOTI_CANDIDATO; LISTA; VOTI_LISTA

### Senato — Epoca 5 Rosatellum (2022)
`Senato_Italia_LivComune.csv` — 19 colonne:
DATAELEZIONE; CODTIPOELEZIONE; CIRC-REG; COLLPLURI; COLLUNINOM; COMUNE; ELETTORITOT; ELETTORIM; VOTANTITOT; VOTANTIM; SKBIANCHE; VOTILISTA; DESCRLISTA; COGNOME; NOME; LUOGONASCITA; DATANASCITA; SESSO; VOTICANDIDATO

## Note
- Delimitatore CSV: `;`, encoding UTF-8, header in prima riga
- Nomi comuni in MAIUSCOLO — normalizzare per join
- Codice ISTAT non presente — serve lookup table
- Camera 1994 II turno (19940529) NON disponibile come ZIP → 404

## Cross dataset
- irpef_comunale (comune) — voto vs reddito
- dait_amministratori_locali (comune) — colore politico vs voto
- popolazione_istat_comunale (comune) — astensione vs demografia
- ispra_ru_base (comune) — voto vs ambiente
- consip_consumi_convenzione (comune) — voto vs spesa pubblica
