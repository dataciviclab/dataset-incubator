# ga-ordinanze — Ordinanze Giustizia Amministrativa (OpenGA)

Dataset unificato delle ordinanze del Consiglio di Stato e dei Tribunali Amministrativi Regionali, proveniente dal portale [OpenGA](https://openga.giustizia-amministrativa.it) della Giustizia Amministrativa.

## Copertura

- **31 sedi**: CdS (appello), CGA Sicilia, 27 TAR, 2 TRGA (Bolzano, Trento)
- **4 anni**: 2023, 2024, 2025, 2026 (aggiornamento MONTHLY)
- **~15.000 ordinanze** totali

## Schema clean (17 colonne)

| Colonna | Tipo | Note |
|---|---|---|
| `anno` | BIGINT | Anno pubblicazione |
| `codice_sede` | BIGINT | Codice sede giudiziaria |
| `nome_sede` | VARCHAR | Nome sede (es. TAR LAZIO - ROMA, CdS GIURISDIZIONALE - ROMA) |
| `codice_sezione` | VARCHAR | Sezione interna |
| `nome_sezione` | VARCHAR | Nome sezione |
| `numero_provvedimento` | BIGINT | PK del provvedimento |
| `numero_ricorso` | BIGINT | **Chiave di join** con sentenze, appalti e ANAC |
| `data_pubblicazione` | DATE | Data pubblicazione ordinanza |
| `mese_pubblicazione` | BIGINT | Mese pubblicazione (formato YYYYMM) |
| `esito_provvedimento` | VARCHAR | Esito (ACCOGLIE, RESPINGE, ecc.) |
| `flg_definisce` | VARCHAR | Flag che definisce il ricorso |
| `data_deposito_ricorso` | DATE | Data deposito ricorso |
| `oggetto_ricorso` | VARCHAR | Descrizione del caso |
| `tipo_ricorso` | VARCHAR | Rito (ORDINARIO, RITO APPALTI, ecc.) |
| `tipo_udienza` | VARCHAR | Pubblica, Camera di Consiglio |
| `num_membri_collegio` | BIGINT | Numero giudici |
| `tipo_provvedimento` | VARCHAR | Tipo (ORDINANZA) |

## Chiavi di join

- `NUMERO_RICORSO` ↔ `ga-sentenze`, `ga-decreti`, `openga-ricorsi-appalto`
- `NUMERO_RICORSO` è univoco a livello nazionale, non per sede

## Fonti

31 dataset CKAN dal portale OpenGA, uno per sede giudiziaria. Schema identico al 100%.

## Mart

| Tabella | Descrizione |
|---|---|
| `mart_esiti_per_sede` | Esiti per sede/anno |
| `mart_esiti_per_tipo` | Esiti per tipo ricorso/anno |
