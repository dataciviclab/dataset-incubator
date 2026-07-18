# ANAC — Aggiudicazioni

**Dataset**: `anac_aggiudicazioni`
**Fonte**: ANAC — Autorità Nazionale Anticorruzione, portale [dati.anticorruzione.it](https://dati.anticorruzione.it/)
**Protocollo**: CKAN (via dati.gov.it + API diretta)
**Licenza**: CC BY 4.0 (Creative Commons Attribuzione 4.0 Internazionale)

## Contenuto

Informazioni di aggiudicazione relative agli appalti ordinari pubblicati dalle stazioni appaltanti italiane. Ogni riga rappresenta un'aggiudicazione identificata da CIG (Codice Identificativo Gara) con:

- **Importo**: importo di aggiudicazione, ribasso
- **Tempi**: data aggiudicazione definitiva, data comunicazione esito
- **Partecipazione**: numero offerte ammesse/escluse, imprese offerenti/richiedenti/invitate
- **Asta elettronica**: flag, modalità
- **Esito**: cod_esito, criterio di aggiudicazione
- **Subappalto**: flag subappalto
- **Collegamento**: id_aggiudicazione (per join con `aggiudicatari`)

## Copertura

Dataset cumulativo full — storico completo delle aggiudicazioni fino alla data di pubblicazione del dump.

**Copertura temporale**: 2000-2026 (dati consistenti da 2007, pre-2007 sporadici)

| Metrica | Valore |
|---|---|
| Righe (full dump 2026-01) | ~4.86M |
| Peso CSV zippato (full) | ~759 MB |
| Peso CSV scomposto | ~2-3 GB |
| Aggiornamento | Mensile (full dump sostituito, delta non inclusi) |
| Anni con copertura solida | 2007-2026 |

## Schema clean (28 colonne)

| Colonna | Tipo | Descrizione |
|---|---|---|
| `cig` | VARCHAR | Codice Identificativo Gara (chiave di join con `anac_bandi_gara`; non univoco — uno stesso CIG può avere più lotti/aggiudicazioni) |
| `data_aggiudicazione_definitiva` | DATE | Data aggiudicazione definitiva |
| `esito` | VARCHAR | Esito aggiudicazione |
| `criterio_aggiudicazione` | VARCHAR | Criterio di aggiudicazione |
| `data_comunicazione_esito` | DATE | Data comunicazione esito |
| `numero_offerte_ammesse` | INTEGER | Offerte ammesse |
| `numero_offerte_escluse` | INTEGER | Offerte escluse |
| `importo_aggiudicazione` | DOUBLE | Importo di aggiudicazione |
| `ribasso_aggiudicazione` | DOUBLE | Ribasso percentuale |
| `num_imprese_offerenti` | INTEGER | Imprese offerenti |
| `flag_subappalto` | BOOLEAN | Flag subappalto |
| `id_aggiudicazione` | BIGINT | ID aggiudicazione (join con `aggiudicatari`) |
| `cod_esito` | INTEGER | Codice esito |
| ... | | Altre colonne raw |

## Join possibili

| Dataset | Chiave | Descrizione |
|---|---|---|
| `anac_bandi_gara` | `cig` | Bando di gara → aggiudicazione |
| `anac_aggiudicatari` (futuro) | `id_aggiudicazione` | Aggiudicazione → vincitore |

## Mart

Due tabelle mart disponibili:

- **`mart_aggiudicazioni_annuale`** — aggregazione per anno/mese/esito/criterio/flag (analisi trend)
  - Colonna: importo_totale, importo_medio/mediano, n_aggiudicazioni, ribasso_medio, offerte
- **`mart_aggiudicazioni_dettaglio`** — row-level con chiavi per join
  - Preserva `cig`, `id_aggiudicazione`, `importo_aggiudicazione`, `data`, `esito`, `flag_subappalto`
  - Join diretto con `anac_bandi_gara` via `cig`

## Limiti

- Dataset cumulativo: aggiornamento mensile con dump full sostituito periodicamente
- WAF sul portale ANAC: necessario User-Agent browser (via `client.user_agent` in dataset.yml)
- `aggiudicatari` (vincitori) non ancora integrato — disponibile come dataset ANAC separato
