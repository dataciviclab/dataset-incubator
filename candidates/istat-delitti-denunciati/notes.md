# Note sul Dataset ISTAT - Delitti Denunciati

## ℹ️ Descrizione del Flusso
Il dataset viene estratto dal portale **ISTAT Esploradati** tramite endpoint SDMX. Poiché il flusso originale è un XML complesso (formato Generic SDMX), la pipeline è stata strutturata per decodificare i tag gerarchici.

## 🛠️ Logica di Trasformazione (ETL)
- **Layer Clean**: Gestisce il parsing pesante dell'XML. Utilizza espressioni regolari (RegEx) per isolare i blocchi `<generic:Series>` e mappare le dimensioni (Territorio, Reato, Anno).
- **Layer Mart**: Fornisce una vista tabellare pulita e tipizzata, pronta per l'analisi statistica o la visualizzazione.

## 📊 Dettagli sui Dati
- **Copertura Temporale**: Serie storica dal 2010 al 2015.
- **Metriche**: Il valore rappresenta il numero di delitti denunciati per specifica categoria e area geografica.
- **Mapping Reati**: I codici (es. `INTENHOM`, `ARSON`) corrispondono alla classificazione ufficiale ISTAT/Ministeriale dei delitti.

## ⚠️ Avvertenze
- La fonte originale include caratteri speciali e una struttura nidificata che richiede DuckDB per un parsing efficiente via SQL.
- In caso di aggiornamento dei flussi SDMX da parte di ISTAT, verificare la tenuta dei pattern RegEx nel file `clean.sql`.
