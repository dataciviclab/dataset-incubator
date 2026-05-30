# Notes — mim-alunni-corso-eta

## 2026-05-30 — Clean arricchito + gerarchia automatica

- Clean ora fa LEFT JOIN con anagrafica scuole via `{support.scu_anagrafica_statali.mart}`
- Da 6 a 16 colonne: aggiunte regione, provincia, comune, denominazione, grado istruzione, ecc.
- 93% copertura join (7% scuole non trovate in anagrafica — probabilmente chiuse o private)
- **Gerarchia automatica**: dichiarata in dataset.yml via `mart.hierarchy`, il toolkit genera h_naz, h_reg, h_prv senza scrivere SQL
- Rimossi 4 vecchi mart separati per ordine scuola

## Tecnico

- download automatizzato via `url_suffix_by_year`
- `CODICESCUOLA` stabile per join con support dataset anagrafica
- clean: LEFT JOIN con anagrafica scuole (2024)
- gerarchia: il toolkit genera `SELECT grain, SUM(metriche) FROM clean_input GROUP BY grain` per ogni livello
- run completato: 2016-2025 (10 anni) ✅

## Schema

- Clean: ~300-330k righe/anno, 16 colonne (dati alunni + metadati scuola)
- Mart: `mart_alunni` (305k righe/anno, dati per scuola) + h_naz (19) + h_reg (361) + h_prv (1976)

## Analitico

- framing ammesso: trend/pressione demografica scolastica per ordine e territorio
- framing escluso: sovraffollamento o alunni/classe
- Con la gerarchia si puo' partire dal nazionale e drill-down fino al comune

## Cautele

- sec_II ha meno comuni (1391) — dati reali, non errore
- `anno_scolastico` è una stringa `YYYYYY` (es. `202425`)
- 7% di scuole senza regione/provincia/comune — non presenti nell'anagrafica 2024 (scuole chiuse, private, o nuovi istituti)
- Le tabelle gerarchiche includono SOLO le metriche numeriche (`alunni`) — `scuole` va contato con `COUNT(DISTINCT codice_scuola)`
