# Note tecniche — elezioni-politiche-2022

## Fonte

**Eligendo** — Archivio storico elettorale del DAIT (Ministero dell'Interno)
- Pagina: https://elezionistorico.interno.gov.it/eligendo/opendata.php
- File: https://dait.interno.gov.it/documenti/opendata/catalogoagid/
- Catalogo AGID (formato CSV diretto, non ZIP)

### File sorgente

| Camera | Senato |
|---|---|
| `camera-2022-Italia-livcomune.csv` (25MB) | `senato-2022-italia-livcomune.csv` (1MB) |

Entrambi: CSV UTF-8, delimitatore `;`, header in prima riga.

## Schema clean (19 colonne)

| Colonna | Tipo | Descrizione |
|---|---|---|
| `data_elezione` | DATE | Data elezione (2022-09-25) |
| `cod_tipo_elezione` | VARCHAR | 'C' = Camera, 'S' = Senato |
| `circoscrizione` | VARCHAR | Circoscrizione elettorale (es. "PIEMONTE 1") |
| `collegio_plurinominale` | VARCHAR | Collegio plurinominale |
| `collegio_uninominale` | VARCHAR | Collegio uninominale |
| `comune` | VARCHAR | Denominazione comune |
| `elettori_totali` | BIGINT | Elettori iscritti totali |
| `elettori_maschi` | BIGINT | Elettori maschi |
| `votanti_totali` | BIGINT | Votanti totali |
| `votanti_maschi` | BIGINT | Votanti maschi |
| `schede_bianche` | BIGINT | Schede bianche |
| `voti_lista` | BIGINT | Voti alla lista (proporzionale) |
| `descr_lista` | VARCHAR | Nome della lista (es. "PARTITO DEMOCRATICO - ITALIA DEMOCRATICA E PROGRESSISTA") |
| `cognome_candidato` | VARCHAR | Cognome candidato uninominale |
| `nome_candidato` | VARCHAR | Nome candidato uninominale |
| `luogo_nascita_candidato` | VARCHAR | Luogo di nascita candidato |
| `data_nascita_candidato` | DATE | Data di nascita candidato |
| `sesso_candidato` | VARCHAR | Sesso candidato ('M'/'F') |
| `voti_candidato` | BIGINT | Voti al candidato uninominale |

## Granularità

Ogni riga = 1 comune × 1 lista × 1 candidato uninominale.
Una lista presente in più collegi uninominali dello stesso comune produce più righe.
Una lista senza candidato (solo proporzionale) produce righe con voti_lista ma voti_candidato = NULL (ma nel dataset 2022 tutte le liste avevano candidati).

## Volumi

| Camera | Senato |
|---|---|
| 117.591 righe | 117.510 righe |
| 7.824 comuni | 7.545 comuni |
| 23 liste | 22 liste |
| 1.247 MB parquet | |

## Qualità dati

- Nomi comuni in MAIUSCOLO (es. "ROMA", "MILANO") — normalizzare per join
- Codice ISTAT non presente — serve lookup table comuni per join preciso
- Circoscrizioni con codice "ESTERO" per voti dall'estero
- Candidati uninominali: alcuni comuni possono avere più candidati per lista (es. Valle d'Aosta)

## Mart

`mart_voti_lista_comune`: aggregazione per comune × lista, con totale voti e conteggio candidati uninominali.

## Join testati

- `comune` (testo) → join approssimativo. Per join preciso serve `codice_istat` da aggiungere in un prossimo giro.

## Per estendere ad altri anni

I file ZIP degli anni precedenti hanno formati diversi (v. issue #523 per lo scout completo):
- 2018: TXT, 17 colonne, schema simile ma nomi diversi
- 2013: TXT, 10 colonne (solo lista, no uninominale)
