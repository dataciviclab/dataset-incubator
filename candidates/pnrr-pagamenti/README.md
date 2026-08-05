# PNRR Pagamenti — Italia Domani

I pagamenti registrati per i progetti PNRR (fonte ReGiS): per ogni progetto (CUP/CLP) il finanziamento totale e PNRR, i pagamenti effettivi (totale, quota PNRR e riparto per fonte) e la data di estrazione.

**211.901 righe**, **€101,9 mld pagamenti PNRR** (estrazione 13/06/2026).

## Dati (23 colonne clean)

- **Chiavi di join**: `cup`, `codice_locale_progetto` (→ `pnrr_progetti`)
- **Classificazione**: `codice_univoco_submisura`, `descrizione_submisura`
- **Finanziamenti**: totale, quota PNRR
- **Pagamenti**: totale, quota PNRR, e riparto per 14 fonti (Stato, Bilancio, FOI, FPOP, UE, Regione, Provincia, Comune, Altro Pubblico, Privato, da Reperire, PNC, Altri Fondi)
- **Data**: estrazione

## Fonte

**Italia Domani** — MEF / SoGeI (fonte ReGiS)
URL: https://www.italiadomani.gov.it/content/dam/sogei-ng/opendata/PNRR_Pagamenti_di_Progetto.csv
Dimensione: ~40 MB, CSV `;` UTF-8 con BOM, importi in formato italiano (virgola decimale), date DD/MM/YYYY.

**Accesso**: il server AEM/Akamai blocca curl/wget e python-requests senza header browser completi. Il `preprocess.py` usa `HttpClient` di `lab-connectors` con `Accept` + `Accept-Language`. Nota: il probe HEAD/GET Range fallisce (404) su questo endpoint; il GET completo funziona e il contenuto può arrivare gzip (gestito nel preprocess).

## Mart

| Tabella | Grano | Contenuto |
|---|---|---|
| `mart_submisura` | submisura | n progetti, finanziamenti, pagamenti e **tasso di assorbimento PNRR** per submisura |
| `mart_sintesi` | nazionale (1 riga) | totali finanziamenti/pagamenti e tasso di assorbimento complessivo |
