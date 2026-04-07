# Note candidate - ISTAT IPAB regionale

## Parametri tecnici
- Flow ISTAT: `143_497` (IPAB - Indice Prezzi Abitazioni)
- Base URL SDMX: `https://esploradati.istat.it/SDMXWS/rest`
- Filtri obbligatori: `IND_TYPE=59` (indice trimestrale), `MISURA1=4` (numeri indici)
- Misure: `ABIT_COMPRAV = NEW_DW` (nuove) e `EXST_DW` (esistenti)
- Granularità: regionale (`ITTER107`)
- Perimetro v0: serie 2020-2025, livello regionale

## Caveat
- `/all` fragile su questo flow: slicing obbligatorio, evitare richieste senza filtri.
- NEW_DW e EXST_DW vanno letti separatamente (nuove vs esistenti).
- L'indice misura variazione relativa rispetto alla base ISTAT, non prezzo assoluto.

## Collegamento
- Discussion: https://github.com/orgs/dataciviclab/discussions/148
