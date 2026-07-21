# ga-sentenze — Sentenze Giustizia Amministrativa (OpenGA)

Dataset unificato delle sentenze del Consiglio di Stato e dei Tribunali Amministrativi Regionali, proveniente dal portale [OpenGA](https://openga.giustizia-amministrativa.it) della Giustizia Amministrativa.

## Copertura

- **31 sedi**: CdS (appello), CGA Sicilia, 27 TAR, 2 TRGA (Bolzano, Trento)
- **4 anni**: 2023, 2024, 2025, 2026 (aggiornamento MONTHLY)
- **~200.000 sentenze** totali

## Schema clean (17 colonne)

| Colonna | Tipo | Note |
|---|---|---|
| `anno` | BIGINT | Anno pubblicazione |
| `codice_sede` | BIGINT | Codice sede giudiziaria |
| `nome_sede` | VARCHAR | Nome sede (es. TAR LAZIO - ROMA) |
| `codice_sezione` | VARCHAR | Sezione interna |
| `nome_sezione` | VARCHAR | Nome sezione |
| `numero_provvedimento` | BIGINT | PK del provvedimento |
| `numero_ricorso` | BIGINT | **Chiave di join** con appalti e ANAC |
| `data_pubblicazione` | DATE | Data pubblicazione sentenza |
| `mese_pubblicazione` | BIGINT | Mese pubblicazione (formato YYYYMM) |
| `esito_provvedimento` | VARCHAR | ACCGLIE, RESPINGE, etc. |
| `flg_definisce` | VARCHAR | Flag che definisce il ricorso |
| `data_deposito_ricorso` | DATE | Data deposito ricorso |
| `oggetto_ricorso` | VARCHAR | Descrizione del caso |
| `tipo_ricorso` | VARCHAR | Rito (APPALTI, ORDINARIO, etc.) |
| `tipo_udienza` | VARCHAR | Pubblica, Camera di Consiglio |
| `num_membri_collegio` | BIGINT | Numero giudici |
| `tipo_provvedimento` | VARCHAR | SENTENZA |

## Chiavi di join

- `NUMERO_RICORSO` ↔ `openga-ricorsi-appalto` (ricorsi appalto)
- `NUMERO_RICORSO` ↔ altri dataset GA (stessa chiave cross-sede)
- `CODICE_CIG` (negli appalti) ↔ dataset ANAC

## Fonti

31 dataset CKAN dal portale OpenGA, uno per sede giudiziaria. Schema identico.

## Mart

| Tabella | Descrizione |
|---|---|
| `mart_esiti_per_sede` | Esiti per sede/anno |
| `mart_esiti_per_tipo` | Esiti per tipo ricorso/anno |
