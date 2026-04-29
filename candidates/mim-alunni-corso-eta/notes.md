# Notes — mim-alunni-corso-eta

## Tecnico

- download automatizzato via `url_suffix_by_year` — URL pattern: `ALUCORSOETASTA{ANNOSCOLASTICO}{DATA}.csv`
- fonte CSV diretta su `catalogo/elements1/`
- `CODICESCUOLA` stabile per join con support dataset anagrafica
- clean: raw-faithful, perdita zero su tutti i 10 anni
- **4 mart**: primaria, sec_I, sec_II, all (tutti per comune) — filtri ordine nel mart SQL
- run completato: 2016-2025 (10 anni) ✅

## Schema

- Clean: ~300-330k righe/anno, colonne: `CODICESCUOLA`, `ORDINE SCUOLA`, `ANNOCORSO`, `FASCIA ETA`, `ALUNNI` + metadata
- Mart primaria: ~5.400-6.300 comuni/anno

## Analitico

- framing ammesso: trend/pressione demografica scolastica per ordine e territorio
- framing escluso: sovraffollamento o alunni/classe

## Cautele

- sec_II ha meno comuni (1391) — dati reali, non errore
- `anno_scolastico` è una stringa `YYYYYY` (es. `202425`) — usare come stringa in join
- mart = INNER JOIN con anagrafica (year=2024) — per anni <2025 alcune scuole chiuse/fuse non sono nell'anagrafica e sono escluse; 2025 perfettamente coincidente
