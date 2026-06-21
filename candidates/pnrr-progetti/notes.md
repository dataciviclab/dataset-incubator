# Note tecniche — pnrr-progetti

## Fonte

**Italia Domani** (MEF / SoGeI)
- Landing page: https://www.italiadomani.gov.it/content/sogei-ng/it/it/catalogo-open-data/Progetti_del_PNRR.html
- URL diretto CSV: https://www.italiadomani.gov.it/content/dam/sogei-ng/opendata/PNRR_Progetti.csv
- Licenza: da verificare (dati pubblici)

## Download

Il server AEM blocca python-requests (anche con User-Agent Mozilla/5.0) ma accetta wget.
Il dataset.yml usa `type: script` con comando wget + sed per rimuovere il BOM.

Per CI: `TOOLKIT_ALLOW_SCRIPT_SOURCE=1` necessario (guardrail di sicurezza).

## Schema clean (63 colonne)

63 colonne, tutte mappate da nomi raw con spazi a nomi normalizzati lowercase_underscore.

### Classificazione
- `programma` — Programma (es. "PNRR")
- `missione` — Codice missione (M1-M7)
- `descrizione_missione` — Nome missione
- `componente` — Codice componente
- `descrizione_componente` — Nome componente
- `id_misura` — ID misura
- `codice_univoco_misura` — Codice univoco misura
- `descrizione_misura` — Nome misura
- `id_submisura` — ID sottomisura
- `codice_cid` — Codice CID
- `codice_univoco_submisura` — Codice univoco sottomisura
- `descrizione_submisura` — Nome sottomisura

### Amministrazione
- `amministrazione_titolare` — Amministrazione titolare (es. "PCM - DIPARTIM. TRASFORMAZIONE DIGITALE")
- `codice_procedura_attivazione` — Codice procedura attivazione
- `titolo_procedura` — Titolo procedura
- `tipologia_procedura_attivazione` — Tipo procedura

### CUP
- `cup` — Codice Unico Progetto (chiave join)
- `codice_locale_progetto` — Codice locale
- `stato_cup` — Stato CUP
- `cup_codice_natura`, `cup_descrizione_natura` — Natura CUP (es. "02: ACQUISTO O REALIZZAZIONE DI SERVIZI")
- `cup_codice_tipologia`, `cup_descrizione_tipologia` — Tipologia
- `cup_codice_settore`, `cup_descrizione_settore` — Settore
- `cup_codice_sottosettore`, `cup_descrizione_sottosettore` — Sottosettore
- `cup_codice_categoria`, `cup_descrizione_categoria` — Categoria

### Progetto
- `titolo_progetto`, `sintesi_progetto` — Descrizione
- `descrizione_tipo_aiuto` — Tipo aiuto (es. "INTERVENTO CHE NON COSTITUISCE AIUTO DI STATO")

### Finanziamenti (14 colonne, DOUBLE)
- `fin_stato` — Finanziamento Stato
- `fin_stato_bilancio` — Finanziamento Stato - Bilancio
- `fin_stato_foi` — Finanziamento Stato - FOI
- `fin_fpop` — Finanziamento FPOP
- `fin_ue` — Finanziamento UE (diverso da PNRR)
- `fin_regione`, `fin_provincia`, `fin_comune` — Enti territoriali
- `fin_altro_pubblico` — Altro pubblico
- `fin_privato` — Privato
- `fin_da_reperire` — Da reperire
- **`fin_pnrr`** — **Finanziamento PNRR** (quota principale)
- `fin_pnc` — Finanziamento PNC
- `altri_fondi` — Altri fondi
- `fin_totale` — Finanziamento totale
- `fin_totale_pubblico` — Totale pubblico
- `fin_totale_pubblico_netto` — Totale pubblico netto

### Soggetto attuatore
- `soggetto_attuatore` — Denominazione
- `cf_soggetto_attuatore` — Codice fiscale

### Tempi
- `flag_progetti_in_essere` — Flag progetti in essere
- `data_inizio_prevista`, `data_inizio_effettiva` — Date inizio
- `data_fine_prevista`, `data_fine_effettiva` — Date fine
- `data_estrazione` — Data estrazione dato
- `data_ultima_validazione` — Data ultima validazione
- `esito_validazione` — Esito

### Stato
- `codice_fase_iter`, `descrizione_fase_iter` — Fase iter progetto
- `stato_fase_iter` — Stato fase
- `stato_avanzamento` — Stato avanzamento (es. "Concluso", "In corso")

## Volumi

| Metrica | Valore |
|---|---|
| Righe | 222.379 |
| Progetti unici (CUP) | 218.240 |
| Missioni | 7 |
| Finanziamento PNRR | €59,2 mld |
| Finanziamento complessivo | €72,1 mld |
| Soggetti attuatori unici | ~5.000+ |
| Dim. parquet | ~100 MB |

## Qualità dati

- Alcune righe CSV hanno quoting problems (gestito con `ignore_errors: true`)
- Finanziamenti: molte colonne sono 0 (non tutte le fonti sono compilate per ogni CUP)
- `data_fine_validita`: VARCHAR perché contiene stringhe non date (es. "non definita" o "31/12/9999")
- `cf_soggetto_attuatore`: alcuni vuoti o placeholder

## Join keys

- `cup` → join con `opencoesione_progetti`, `anac_bandi_gara` (CUP/CIG indiretto), BdAP MOP
- `cf_soggetto_attuatore` → join con `bdap_anagrafe_enti`

## Cross-dataset

| Dataset | Chiave | Domanda |
|---|---|---|
| `anac_bandi_gara` | CUP (via `cui_programma`) | I progetti PNRR diventano gare? |
| `opencoesione_progetti` | CUP | Doppio finanziamento? |
| `bdap_anagrafe_enti` | CF | Chi sono i soggetti attuatori? |
