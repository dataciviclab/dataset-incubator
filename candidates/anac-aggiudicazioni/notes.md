# Note tecniche — anac-aggiudicazioni

## Struttura fonte

CKAN dataset `aggiudicazioni` su dati.anticorruzione.it:
- Full dump: risorsa `aggiudicazioni_csv` (~759MB ZIP)
- Delta mensili: risorse `YYYYMMDD-aggiudicazioni_csv` (XXX MB)
- Senza DataStore — download diretto CSV via filesystem API

Config scelta: solo full dump via `resource_name: "aggiudicazioni_csv"` + extractor `unzip_first_csv`.
Delta mensili esclusi: il full dump è cumulativo, scaricando anche i delta si avrebbero duplicati.

## Schema osservato

Dal delta CSV `20260701-aggiudicazioni_csv.csv` (190.829 righe):

Colonne raw (CSV, delim `;`, quoted `"`):
cig, data_aggiudicazione_definitiva, esito, criterio_aggiudicazione,
data_comunicazione_esito, numero_offerte_ammesse, numero_offerte_escluse,
importo_aggiudicazione, ribasso_aggiudicazione, num_imprese_offerenti,
flag_subappalto, id_aggiudicazione, cod_esito, num_imprese_richiedenti,
asta_elettronica, num_imprese_invitate, massimo_ribasso, minimo_ribasso,
FLAG_SCOMPUTO, COD_PRESTAZIONI_COMPRESE, PRESTAZIONI_COMPRESE,
CIG_PROG_ESTERNA, DATA_INCARICO_PROG, DATA_CONS_PROG,
COD_MODO_RIAGGIUDICAZIONE, MODO_RIAGGIUDICAZIONE,
FLAG_PROC_ACCELERATA, N_MANIF_INTERESSE

## Join chain

anac_bandi_gara (cig) ←→ anac_aggiudicazioni (cig)
anac_aggiudicazioni (id_aggiudicazione) ←→ aggiudicatari (id_aggiudicazione)

Note: id_aggiudicazione con valori negativi (-1, -2xxxx) indica
aggiudicazioni senza corrispondenza in anagrafica aggiudicatari.

## Warning ANAC WAF

Il portale dati.anticorruzione.it blocca richieste senza User-Agent browser.
Già risolto in anac-bandi-gara con `client.user_agent` config.

## Qualità dati (run 2026-07-18)

| Metrica | Valore |
|---|---|
| Metrica | Valore |
|---|---|
| Righe totali | 4.862.077 |
| CIG distinti | 4.849.388 |
| Con importo | 4.838.224 (99,5%) |
| Con data valida | 4.819.598 (99,1%) |
| Importo totale (aggiudicato) | €3.934 Mld |
| Importo mediano | €50.000 |
| CIG / id_aggiudicazione nulli | 0 ✅ |

**Anomalie note (non bloccanti):**
- 2.221 date fuori range (anno < 2000 o > 2026) — date malformate nel sorgente
- 369 importi negativi — probabili storni/rettifiche
- 34.314 importi zero con esito "AGGIUDICATA" — aggiudicazioni senza importo comunicato
- 12.689 CIG con più righe (0,3%) — uno stesso CIG può avere più lotti/aggiudicazioni
- 69% dei record senza criterio di aggiudicazione (NULL)
- Discontinuità 2024+: esplosione volumi (382K → 1,2M), crollo subappalti dichiarati — probabile cambio normativo (D.Lgs 36/2023) o metodologia ANAC

**Schema verificato**: full dump conforme al delta osservato. Separatore decimale "." (già processabile da DuckDB). Flag booleani in formato stringa "true"/"false".
