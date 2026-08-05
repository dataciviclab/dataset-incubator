# PNRR Progetti

Tutti i progetti del Piano Nazionale di Ripresa e Resilienza (PNRR) con dettaglio CUP, missione, componente, misura, finanziamenti per 14 fonti, soggetto attuatore e stato avanzamento.

**291.398 righe**, **285.994 progetti** (CUP unici), **€144,0 mld PNRR**, **€206,9 mld complessivi**.

## Dati

63 colonne, divise in:
- **Classificazione**: programma, missione (7), componente, misura, sottomisura
- **CUP**: codice, stato, natura, tipologia, settore, sottosettore, categoria
- **Progetto**: titolo, sintesi, tipo aiuto
- **Finanziamenti**: Stato, Bilancio, FOI, FPOP, UE, Regione, Provincia, Comune, Privato, da Reperire, **PNRR**, **PNC**, Altri, Totale (14 voci)
- **Soggetto attuatore**: denominazione, CF
- **Tempi**: date inizio/fine previste/effettive
- **Stato**: avanzamento, fase iter, validazione

## Fonte

**Italia Domani** — MEF / SoGeI
URL: https://www.italiadomani.gov.it/content/dam/sogei-ng/opendata/PNRR_Progetti.csv
Dimensione file: ~317 MB
Encoding: UTF-8 con BOM
Download: `preprocess.py` (wget + fallback urllib) — il server AEM/Akamai
blocca python-requests ma accetta wget (pattern verificato in CI)

## Mart

| Tabella | Grano | Contenuto |
|---|---|---|
| `mart_missione` | missione × componente | n progetti, finanziamenti PNRR e totali per missione/componente |
| `mart_stato_avanzamento` | stato avanzamento | n progetti, finanziamenti e % sul totale per stato (In Corso / Concluso / Da Attivare) |

## Issue

#518 — Intake PNRR Progetti
