# Notes

## Tecnico

- fonte demo ISTAT `POSAS`
- pattern URL verificato per `2019-2025`
- file ZIP annuale con un solo CSV
- il CSV osservato per `2025` usa `;` come delimitatore e `utf-8` con BOM
- il primo record del file e una riga titolo da saltare
- la chiave naturale per join e `codice_comune`
- `eta = 999` rappresenta il totale comunale e va trattato separatamente dalle eta puntuali
- run verificati: `2019`, `2020`, `2025`
- il rilancio completo `2019-2025` ha incontrato un `PermissionError` locale su `out/data/_runs` nel `2021`, probabile lock filesystem / OneDrive piu che problema di schema

## Analitico

- dataset infrastrutturale prima che filone narrativo autonomo
- il valore principale e supportare join, controlli pro capite e coverage check
- il dettaglio per eta puo servire anche come base per futuri indicatori di struttura demografica
- join di prova con `IRPEF 2023`: `7892` match su `7897` comuni (`99,94%`)
- i pochi non match emersi confermano che il dataset e gia utile come detector di anomalie territoriali

## Cautele

- verificare variazioni territoriali e fusioni di comuni nel periodo
- non assumere subito piena stabilita di schema senza run reale su piu anni
- trattare `comune` come descrittivo e `codice_comune` come chiave primaria di lavoro
