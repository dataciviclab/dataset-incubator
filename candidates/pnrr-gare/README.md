# PNRR Gare — Italia Domani

Le gare d'appalto dei progetti PNRR pubblicate da Italia Domani (fonte ReGiS): per ogni gara il collegamento **CUP → CIG**, gli importi complessivo e di aggiudicazione, la procedura, la modalità di realizzazione e l'oggetto del contratto.

**282.655 righe**, **244.510 CIG unici**, **63.499 CUP unici**. ~25.250 gare senza CIG (motivazione per legge: in-house, accordi tra amministrazioni, concessioni, ecc.).

## Dati (19 colonne clean)

- **Chiavi di join**: `cup` (→ `pnrr_progetti`, `anac_cup`, OpenCoesione), `cig` (→ ANAC)
- **Classificazione**: `codice_univoco_submisura`, `descrizione_submisura`
- **Gara**: procedura di aggiudicazione, modalità realizzazione, oggetto principale, oggetto gara
- **Importi**: `importo_complessivo_gara`, `importo_aggiudicazione`
- **Date**: pubblicazione CIG, aggiudicazione definitiva, estrazione
- **CIG**: `cig`, `cig_accordo_quadro`, codice/descrizione motivo assenza CIG

## Fonte

**Italia Domani** — MEF / SoGeI (fonte ReGiS)
URL: https://www.italiadomani.gov.it/content/dam/sogei-ng/opendata/PNRR_Gare.csv
Dimensione: ~106-111 MB, CSV `;` UTF-8 con BOM, importi in formato italiano (virgola decimale), date DD/MM/YYYY.

**Accesso**: il server AEM/Akamai blocca curl/wget e python-requests senza header browser completi. Il `preprocess.py` usa `HttpClient` di `lab-connectors` con `Accept` + `Accept-Language` (validato: HTTP 200).

## Issue

#517 — Intake PNRR Gare (aperta, non lavorata)

## Mart

| Tabella | Grano | Contenuto |
|---|---|---|
| `mart_submisura` | submisura | n gare/CIG/CUP, importi complessivo e aggiudicato |
| `mart_procedura` | procedura | n gare, importo per tipo procedura |
