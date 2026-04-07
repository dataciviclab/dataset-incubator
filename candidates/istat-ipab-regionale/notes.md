# Note candidate - ISTAT IPAB aree

## Parametri tecnici
- Flow ISTAT: `143_497` (IPAB - Indice Prezzi Abitazioni)
- Base URL SDMX: `https://esploradati.istat.it/SDMXWS/rest`
- Dimensioni usate nel fetch: `DATA_TYPE=59`, `MEASURE=4`, `PURCHASES_DWELLINGS = NEW_DW/EXST_DW`, `FREQ=Q`
- Copertura osservata nel v0: Italia, 4 macro-aree e 3 citta
- Perimetro v0: serie trimestrale completa 2010-2025 su aree aggregate, non su regioni NUTS2

## Caveat
- `/all` fragile su questo flow: slicing obbligatorio, evitare richieste senza filtri.
- `NEW_DW` e `EXST_DW` vanno letti separatamente (nuove costruzioni vs abitazioni esistenti).
- L'indice misura variazione relativa rispetto alla base ISTAT, non prezzo assoluto.
- La copertura non e regionale: il dato non consente confronti diretti tra singole regioni.

## Collegamento
- Discussion: https://github.com/orgs/dataciviclab/discussions/148
