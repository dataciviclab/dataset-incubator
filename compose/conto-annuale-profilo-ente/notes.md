# Note — Conto Annuale Profilo Ente

## Note tecniche

- **Fonte**: 6 clean parquet su GCS (occupazione, personale, anzianità, titoli-studio, composizione-retribuzione, costo-lavoro, assenze)
- **Join**: su `istituzione + anno + codi_comparto`
- **Età media**: media pesata con centro fascia (E0=15, E20=22, ..., E68=71)
- **Anzianità media**: media pesata con centro fascia (A0=2.5, A6=8, ..., A44=47)
- **% Laureati**: include LAUREA, LAUREA BREVE, SPECIALIZZAZIONE, DOTTORATO, ALTRI TITOLI POST LAUREA
- **NB**: non tutti gli enti hanno dati in tutti i dataset — LEFT JOIN gestisce i missing
