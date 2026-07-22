# ga-decreti — Decreti Giustizia Amministrativa (OpenGA)

Dataset unificato dei decreti del Consiglio di Stato e dei Tribunali Amministrativi Regionali, proveniente dal portale [OpenGA](https://openga.giustizia-amministrativa.it) della Giustizia Amministrativa.

## Copertura

- **31 sedi**: CdS (appello), CGA Sicilia, 27 TAR, 2 TRGA (Bolzano, Trento)
- **4 anni**: 2023, 2024, 2025, 2026 (aggiornamento MONTHLY)
- **~7.500 decreti** totali

## Schema clean (17 colonne)

| Colonna | Tipo | Note |
|---|---|---|
| `anno` | BIGINT | Anno pubblicazione |
| `codice_sede` | BIGINT | Codice sede giudiziaria |
| `nome_sede` | VARCHAR | Nome sede (es. TAR LAZIO - ROMA) |
| `codice_sezione` | VARCHAR | Sezione interna |
| `nome_sezione` | VARCHAR | Nome sezione |
| `numero_provvedimento` | BIGINT | PK del provvedimento |
| `numero_ricorso` | BIGINT | **Chiave di join** con sentenze, ordinanze, appalti |
| `data_pubblicazione` | DATE | Data pubblicazione decreto |
| `mese_pubblicazione` | BIGINT | Mese pubblicazione (formato YYYYMM) |
| `esito_provvedimento` | VARCHAR | Esito |
| `flg_definisce` | VARCHAR | Flag che definisce il ricorso |
| `data_deposito_ricorso` | DATE | Data deposito ricorso |
| `oggetto_ricorso` | VARCHAR | Descrizione del caso |
| `tipo_ricorso` | VARCHAR | Rito |
| `tipo_udienza` | VARCHAR | Pubblica, Camera di Consiglio |
| `num_membri_collegio` | BIGINT | Numero giudici |
| `tipo_provvedimento` | VARCHAR | Tipo (DECRETO) |

## Chiavi di join

- `NUMERO_RICORSO` ↔ `ga-sentenze`, `ga-ordinanze`, `openga-ricorsi-appalto`

## Mart

| Tabella | Descrizione |
|---|---|
| `mart_esiti_per_sede` | Esiti per sede/anno |
| `mart_esiti_per_tipo` | Esiti per tipo ricorso/anno |
