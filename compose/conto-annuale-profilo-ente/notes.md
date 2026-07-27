# Note — Conto Annuale Profilo Ente

## Note tecniche

- **Fonte**: 6 clean parquet su GCS (occupazione, personale, anzianità, titoli-studio, composizione-retribuzione, costo-lavoro, assenze)
- **Join**: su `istituzione + anno + codi_comparto`
- **Età media**: media pesata con centro fascia (E0=15, E20=22, ..., E68=71)
- **Anzianità media**: media pesata con centro fascia (A0=2.5, A6=8, ..., A44=47)
- **% Laureati**: include LAUREA, LAUREA BREVE, SPECIALIZZAZIONE, DOTTORATO, ALTRI TITOLI POST LAUREA
- **NB**: non tutti gli enti hanno dati in tutti i dataset — LEFT JOIN gestisce i missing
- **Join esterni**: `codi_fiscale` → `ipa_enti` (partita IVA), `istituzione` → `bdap_anagrafe_enti` (codice BDAP)
- **Anni**: 2020-2024 (5 anni). Il 2020 è disponibile su GCS ma alcuni dataset (assenze) potrebbero avere copertura parziale
- **Soglia enti**: i mart escludono enti con meno di 5 dipendenti (metriche procapite distorte)
- **Medie nel mart comparto**: `eta_media` e `anzianita_media` sono **medie non pesate** (ogni ente pesa 1, non in proporzione ai dipendenti). Per la media pesata reale, usare `tot_dipendenti` e le somme dal clean
