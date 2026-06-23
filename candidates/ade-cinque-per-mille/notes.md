# Note tecniche — ade-cinque-per-mille

## Raw
- Script: `scripts/download_5x1000.py`
- Scarica 7 parti CSV per anno e le concatena
- Le parti sono divise per iniziale/categoria dell'ente
- Usa URL guest di Liferay (pattern: .../documents/d/guest/5x1000-af{year}...)
- `ignore_errors: true` per gestire righe di nota legale nei CSV originali

## Clean
- 19 colonne, 90.611 righe (2024)
- I flag categoria (ETS, ASD, ricerca, ecc.) sono booleani
- Gli importi usano formato italiano (. migliaia, , decimali) convertiti via REPLACE
- `read_mode: strict` per evitare sniffing automatico di DuckDB

## Mart
- Aggregazione per regione (21 regioni)

## Da fare
- [ ] Aggiungere anni 2022 e 2023 (URL guest da trovare)
- [ ] Verificare se il 2025 esiste in CSV
