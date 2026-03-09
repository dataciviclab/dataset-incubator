# Notes — malasanita-struttura-mortalita

## Stato verifica — da dichiarare a @Gabrymi93 prima di aprire l'issue preanalysis

Le fonti A, B, C reggono il flusso canonico RAW → CLEAN → MART senza passaggi manuali.
La fonte D è disponibile, completa e scaricabile senza login, ma richiede uno step extra
(unzip + lettura XLSX) che non è un blocco ma va dichiarato esplicitamente.

**Azione:** applicare path hardenizzato su file esplicito per D e proseguire con clean/mart.

Opzioni per la fonte D:
1. Usare `http_file` + extractor ZIP del toolkit (`unzip_first`) ✅ testato
2. Pre-processare D localmente → esportare CSV → trattare come `local_file` nel dataset.yml
3. Scrivere un custom step di pre-ingest in Python prima del run

## Verifica fonti (stato al 2026-03-09)

| ID | Fonte | URL diretto | HTTP | Formato | Anno | Dimensione | Autenticazione |
|---|---|---|---|---|---|---|---|
| A | Strutture e attività ASL | https://www.dati.salute.gov.it/sites/default/files/2024-05/Strutture_e_attivit%C3%A0_ASL.csv | 200 ✅ | CSV | 2022 | 24 KB | nessuna |
| B | Reparti strutture di ricovero | https://www.dati.salute.gov.it/sites/default/files/2024-05/Dati_di_anagrafe_e_di_attivit%C3%A0_delle_Strutture_di_Ricovero_Pubbliche_ed_equiparate.csv | 200 ✅ | CSV | 2022 | 2,4 MB | nessuna |
| C | Strutture ricovero per ASL | https://www.dati.salute.gov.it/sites/default/files/2025-01/Strutture_di_ricovero_pubbliche_presenti_nel_territorio_della_ASL.csv | 200 ✅ | CSV | 2022 | 144 KB | nessuna |
| D | Mortalità per causa — ISTAT | https://www.istat.it/wp-content/uploads/2025/09/Tavole.zip | 200 ✅ | ZIP→XLSX | 2022 | 3,6 MB | nessuna |

## Tecnico

### Fonti A, B, C — Ministero della Salute

- Delimitatore: `;`
- Encoding: non verificato (presumibile latin-1 o utf-8-sig — da testare in ingest)
- Chiave regionale: `Codice Regione` (fonte A) / `codice_regione` (fonti B, C) — codice numerico 3 cifre (es. `010` = Piemonte)
- Anno confermato in dati: `2022` (colonna `Anno di Riferimento` / `anno`)

**Colonne chiave fonte A (Strutture e attività ASL):**
`Anno di Riferimento`, `Codice Regione`, `Regione`, `Totale medici`, `Totale pediatri`, `Totale scelte per classe di scelte`, `Numero medio medici titolari`, granularità ASL

**Colonne chiave fonte B (Reparti strutture di ricovero):**
`anno`, `codice_regione`, `regione`, `codice_disciplina`, `disciplina`, `posti_letto_day_hospital`, `posti_letto_degenza_ordinaria`, `num_dimessi`, `giornate_degenza`, granularità reparto/struttura

**Colonne chiave fonte C (Strutture ricovero per ASL):**
`anno`, `codice_struttura`, `codice_regione`, `Regione`, `totale_personale`, `medici`, `infermieri`, `posti_letto_previsti`, granularità struttura

### Fonte D — ISTAT Mortalità per causa 2022

**Situazione portale:** il portale dati.istat.it è irraggiungibile (redirect a avvisi.istat.it). I dati sono accessibili tramite pagina statica ISTAT.

**File:** `Tavole.zip` → `Tavole/data_base_2022.xlsx` → foglio `d_base_2022`

**Struttura colonne:**
`anno`, `Cod_Territorio`, `Territorio`, `Cod_Sesso`, `Sesso`, `Cod_Classe età`, `Classe età`, `Cod_Titolo di studio`, `Titolo di studio`, `Cod_Causa`, `Causa`, `pop media`, `decessi`, `tassi_standardizzati per 10.000`

**Territori presenti:** tutte le regioni italiane incluse Valle d'Aosta, Bolzano, Trento + aggregati macro-area + ITALIA

**25 cause di morte raggruppate** (es. "Malattie del sistema circolatorio", "Tumori", "Malattie cerebrovascolari", "Covid-19", ecc.)

**Granularità:** regione × causa × sesso × classe età × titolo di studio — richiede aggregazione per ottenere totali regionali

**Compatibilità toolkit (esito test):** `http_zip` non è un plugin disponibile. Il path nativo funzionante è `type: http_file` con `extractor: unzip_first`, ma dipende dall'ordine interno del ZIP.

**Hardening applicato:** il dataset principale resta runnable da clone pulito con `http_file + unzip_first`. Per maggiore controllo e disponibile uno script opzionale (`scripts/prepare_source_d.ps1`) che estrae esplicitamente `data_base_2022.xlsx` in `inputs/` senza lasciare artefatti temporanei nel repository.

**Definizione "mortalità evitabile":** non è una colonna diretta — va operazionalizzata selezionando le cause pertinenti tra le 25 disponibili (es. metodologia Euro-2013 o scelta ragionata). Questo è un passaggio metodologico da documentare esplicitamente.

## Chiave di join regionale

- Fonti A/B/C usano codice regione numerico 3 cifre (es. `010` per Piemonte)
- Fonte D usa nome regione testuale (es. `PIEMONTE`)
- Il join richiede una tabella di corrispondenza codice_regione ↔ nome_regione ISTAT
- 21 unità territoriali (19 regioni + 2 province autonome Bolzano e Trento)

## Analitico

- Domanda: correlazione struttura sanitaria (personale) ↔ mortalità evitabile per regione, anno 2022
- Unità di analisi: regione (aggregare le fonti A/B/C da granularità ASL/struttura)
- Asse principale: medici e infermieri per 100.000 ab. vs tasso mortalità evitabile per 100.000 ab.
- Dati popolazione per il denominatore: usare `pop media` dalla fonte D o fonte esterna (ISTAT POSAS)

## Cautele

- **Gap temporale Ministero:** dati strutture (A, B, C) fermi al 2022 — documentare come dato narrativo ("la PA non aggiorna da 3 anni")
- **Fonte D — codice regione assente:** join solo su nome testuale → rischio errori su nomi con spazi/accenti; serve pulizia
- **Mortalità evitabile non è una colonna diretta:** va costruita selezionando cause — scelta metodologica da documentare
- **Emilia-Romagna:** benchmark metodologico opzionale, esclusa dall'analisi principale
- **Titolo di studio nella fonte D:** non necessario per questa analisi, da ignorare nell'aggregazione
- **Fonti di Livello 2** (AGENAS/SIMES, MedMal Marsh): non usare nella preanalysis

## Pagine sorgente (per aggiornamenti futuri)

- A: https://www.dati.salute.gov.it/it/dataset/strutture-e-attivita-asl/
- B: https://www.dati.salute.gov.it/it/dataset/dati-di-struttura-e-di-attivita-dei-reparti-presenti-ciascuna-struttura-di-ricovero/
- C: https://www.dati.salute.gov.it/it/dataset/strutture-di-ricovero-pubbliche-e-equiparate-presenti-nel-territorio-della-asl/
- D: https://www.istat.it/tavole-di-dati/disuguaglianze-nella-mortalita-per-causa-in-italia-secondo-caratteristiche-demografiche-sociali-e-territoriali-anno-2022/
