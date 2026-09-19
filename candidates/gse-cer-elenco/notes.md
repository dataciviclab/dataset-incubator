## Tecnico

- XLSX diretto, toolkit legge con `read_xlsx` automaticamente.
- Granularità: CER per comune. 904 righe originali, 903 dopo dedup (1 duplicato: "COMUNITA' ENERGETICA RINNOVABILE ZONA SICILIA" a San Giovanni Gemini).
- `Potenza totale (kW)` e coordinate usano virgola decimale (formato italiano) — gestito in clean.sql con `replace(',', '.')`.
- `Tipologia di configurazione` è omogenea ("Comunità energetica rinnovabile") — esclusa dal clean in quanto costante.
- `Data di aggiornamento` è 31/12/2025 per tutti i record — snapshot singolo.

## Analitico

- 904 CER, 94,96 MW totali, 8.653 utenze, 1.429 impianti.
- Top regioni per n_cer: Lombardia, Piemonte, Sicilia, Veneto.
- Paradosso potenza: Piemonte leader per kW (~25.000) nonostante meno CER della Lombardia — impianti di taglia media più grande.
- 75,3% delle CER sono micro (<50 kW), ma il 7,2% grande (>500 kW) genera il 64% della potenza.

## Cautele

- Il file contiene 904 CER, ma fonti citano 1.805 configurazioni a dic 2025 — potrebbe essere un sottoinsieme (solo CER, non autoconsumatori/distanti).
- Nessuna serie storica — snapshot singolo, da monitorare per nuove release.
- Fonte: download diretto da sito GSE, non presente su dati.gov.it.
- `area_convenzionale` è il codice cabina primaria — utilile per join con dati rete elettrica.
