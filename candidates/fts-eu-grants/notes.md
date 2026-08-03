# Note tecniche — FTS EU Grants

## Fonte

- **URL XLSX**: `https://ec.europa.eu/budget/financial-transparency-system/download/{YEAR}_FTS_dataset_en.xlsx`
- **Formato**: XLSX, primo sheet
- **Anni**: 2020–2024 verificati funzionanti (2007–2019 disponibili su richiesta)
- **HEAD richiesto**: il server Europa restituisce `Content-Length: 0` su HEAD ma il file è correttamente servito su GET (chunked encoding)
- **Licenza**: EU Open Data

## Pipeline

- `type: script` esegue `scripts/convert_xlsx_to_csv.py` che scarica l'XLSX e produce un CSV normalizzato
- Lo script usa `pandas.read_excel(dtype=str)` per leggere tutto come stringhe, evitando problemi di tipo tra anni
- `clean.read` legge il CSV prodotto dallo script (non l'XLSX diretto)
- Richiede `TOOLKIT_ALLOW_SCRIPT_SOURCE=1` per abilitare lo script source

## ⚠️ Schema XLSX VARIABILE per anno (scoperto 2026-08-03)

| Anni | Colonne | Differenze |
|---|---|---|
| 2020-2023 | 39 | `Recipient main registration number`, `Call for proposals Reference`, `Project / Contract Reference`, `Project / Contract Acronym` |
| 2024 | 38 | `VAT number of beneficiary`, `Geographical Zone`, `Action location`, `Funding type` |

**35 colonne comuni** a tutti gli anni. Lo script mappa **per NOME** (non posizionale) a 38 colonne italiane stabili; colonne assenti nell'anno → vuote. Il vecchio script posizionale era rotto: `df.columns = FTS_COLUMNS` (38) su file da 39 colonne → ValueError, run mai riuscito.

**Perché non http_file+XLSX diretto**: il toolkit legge l'XLSX nativamente ma DuckDB risolve i nomi colonna a parse time → referenziare una colonna 2024-only nel run 2023 fallisce (BinderError). `align_by_header` (schema variabile) è supportato SOLO per CSV, non per Excel. Lo script resta il punto di normalizzazione.

## Importi — formato internazionale (NON italiano)

Gli importi XLSX sono già numerici con **punto decimale** (`29759799.09`), nessuna virgola migliaia — verificato su tutti gli anni. **NON usare `replace('.','')`** (moltiplicherebbe per ~1000): cast diretto a float. Il vecchio script `REPLACE(',', '')` era innocuo (nessuna virgola).

## Metriche consumato — beneficiario vs commitment

- `importo_consumato_stimato` (Beneficiary's estimated consumed) = quota del **beneficiario** → ratio consumato/contrattato sensato (~65-86%)
- `impegno_consumato` (Commitment consumed) = consumo dell'**intero commitment** → ratio > 100%, NON usare per l'assorbimento

## RRF — Recovery and Resilience Facility

Flag `is_rrf` nel clean ('SI'/'NO' su `nome_programma LIKE '%Recovery%'`). Il RRF è un trasferimento di bilancio UE→Stato (non un grant analitico): 2023 = 23,9 mld su 27,9 totali (86%). **Escluso dalle mart analitiche** ma esposto come `importo_rrf_eur` nel trend. Decisione civic-director 2026-08-03 (opzione 3: flag, dato completo preservato).

## Discrepanza vs discussion #395

La discussion cita 9,77 mld contrattati 2020-2024 (Horizon 3,65 mld = 37%). I dati attuali FTS danno **17,05 mld no-RRF** (Horizon 4,75 mld = 28%). Le righe combaciano (40.417 vs 40.449) ma gli importi no → i dati FTS sono stati aggiornati dalla Commissione o la discussion usava un subset diverso. **Da riconciliare con data-researcher** (la discussion va aggiornata o va chiarita la metrica).

## Filtro Italia

Il filtro `paese_beneficiario = 'Italy'` usa il nome completo del paese (non ISO). Copre i beneficiari con sede legale in Italia — non necessariamente i progetti che si svolgono in Italia.

### Differenza con OpenCoesione / RNA

- **FTS** copre solo la gestione diretta UE (Commissione europea)
- **OpenCoesione** copre i fondi strutturali (gestione condivisa con Stati membri)
- **RNA** copre gli aiuti di Stato (erogati da enti italiani, non UE)

## Colonne notevoli

- `beneficiario_nome`: può contenere `*****` per motivi di privacy (persone fisiche)
- `importo_contrattato`: l'importo effettivamente contrattualizzato (può essere vuoto nel 2024 — 1.928 righe)
- `importo_consumato_stimato`: quanto è stato effettivamente speso (stimato)
- `nome_programma`: include il programma UE (es. "1.0.23 - Digital Europe Programme")

## Limiti noti

- I dati FTS coprono solo la gestione diretta UE (~20% del budget UE). I fondi strutturali (80%) sono altrove (OpenCoesione, ESIF, Kohesio).
- Alcuni beneficiari sono offuscati (`*****`) per motivi di privacy.
- I nomi dei programmi non sono normalizzati — il raggruppamento per categoria è fatto nel mart.
- Le date progetto possono essere vuote o `-` (normalizzate a vuoto dallo script, ~1.100 righe in data_fine 2020).
- **PK non dichiarabile a livello riga**: il sorgente FTS contiene righe duplicate reali (stesso rif_impegno + beneficiario + importi + oggetto + date). Anche con 8 campi restano 38 duplicati identici su 8.559 righe (2023). Deroga primary_key (§4 candidate-standard).
