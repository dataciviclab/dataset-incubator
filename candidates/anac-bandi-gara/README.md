# ANAC — Bandi di Gara (CIG)

**Dataset**: `anac_bandi_gara`
**Fonte**: ANAC — Autorità Nazionale Anticorruzione, portale [dati.anticorruzione.it](https://dati.anticorruzione.it/)
**Protocollo**: CKAN (via `dati.gov.it` + API diretta)
**Licenza**: CC-BY-SA 4.0

## Contenuto

Bandi di gara pubblicati dalle stazioni appaltanti italiane, identificati dal CIG (Codice Identificativo Gara). Ogni riga rappresenta un lotto di gara con informazioni su:

- **Oggetto**: descrizione, importo, CPV, CIG accordo quadro
- **Stazione appaltante**: denominazione, CF, AUSA, centro di costo
- **Territorio**: codice ISTAT luogo, provincia
- **Tempi**: pubblicazione, scadenza offerta, esito, cancellazione
- **Procedure**: tipo scelta contraente, modalità realizzazione, urgenza, delega
- **PNRR**: flag PNRR/PNC per gare legate al Piano Nazionale Ripresa e Resilienza
- **Esito**: aggiudicato/non aggiudicato/cancellato

## Copertura

| Anno | Righe | Note |
|---|---|---|
| 2025 | ~1.47M | Primo anno validato (12 mesi, 1.23GB raw → 330MB parquet clean) |
| 2007-2024 | — | Disponibili su portale ANAC, da estendere progressivamente |

## Schema clean (53 colonne)

Le 61 colonne raw vengono tipizzate in clean:
- `cig` (PK), `cig_accordo_quadro`, `numero_gara`
- `importo_complessivo_gara`, `n_lotti_componenti`, `importo_lotto`, `importo_sicurezza`
- `oggetto_gara`, `oggetto_lotto`, `oggetto_principale_contratto`
- `stato`, `settore`, `esito`, `cod_esito`
- `codice_istat_luogo`, `provincia`, `sezione_regionale`
- `data_pubblicazione`, `data_scadenza_offerta`, `data_comunicazione_esito`
- `cf_amministrazione_appaltante`, `denominazione_amministrazione_appaltante`, `codice_ausa`
- `cod_cpv`, `descrizione_cpv`
- `flag_pnrr`, `flag_urgenza`, `flag_delega` (BOOLEAN)
- `anno_pubblicazione`, `mese_pubblicazione`
- tipologia scelta contraente, modalità realizzazione/indizione, durata prevista, strumento svolgimento

## Mart

- **`mart_bandi_annuale`**: aggregazione per anno/mese/provincia/CPV/stato/esito/PNRR con conteggi e importi

## Join possibili

| Dataset | Chiave | Descrizione |
|---|---|---|
| `openga_ricorsi_appalto` | `cig` | Ricorsi in materia d'appalto al Consiglio di Stato (già integrato con ANAC dalla fonte) |
| `bdap_anagrafe_enti` | `cf_amministrazione_appaltante` | Anagrafica enti pubblici (codici IPA, SIOPE, ISTAT) |
| `bdap_mop_gare` | `cig` / `cup` | Gare Opere Pubbliche MOP (BDAP) |
| `consip_consumi_convenzione` | — | Spesa PA in convenzione (analisi complementare) |

## Limiti

- Solo **bandi di gara** (CIG) — non le aggiudicazioni (vincitori). Il dataset ANAC `aggiudicatari` è separato.
- La disponibilità di dati economici (importo lotto, esito) varia per anno: più recenti = più nulli
- WAF sul portale ANAC diretto: necessario User-Agent browser (via `client.user_agent` nel dataset.yml)
- Formato raw variabile per anno (CSV/JSON/TTL): da verificare con `schema_diff` prima di estendere
