# intercettazioni

Bersagli intercettazioni per tipologia, ufficio e distretto.

## Dati

- **Fonte**: Ministero della Giustizia — DG Statistica (datiestatistiche.giustizia.it)
- **File**: `Intercettazioni.xlsx`, sheet "Tutti gli uffici"
- **Copertura**: 2014–2025 (+ anni isolati 1994, 2011)
- **Sheet**:
  - **Tutti gli uffici** (v0): anno, tipo ufficio, distretto, tipologia intercettazione, n. bersagli — 3.953 righe
  - **Tipologia di reato** (v1): aggiunge tipo di reato (ordinaria, DDA/mafia, terrorismo) — 3.589 righe
- **Tipologie intercettazione**: Telefoniche, Ambientali, Informatiche, Trojan
- **Uffici**: Procura ordinaria, Procura Minorenni, Procura Generale
- **Granularità**: distrettuale (26 distretti)
- **Run**: `toolkit run all --config candidates/intercettazioni/dataset.yml --years 2025` ✅
- **Licenza**: dati pubblici (Italian Open Data License v2.0)

## Join possibili

- `distretto` → anagrafe distretti giudiziari

## Valore

Tema di forte interesse pubblico. Distinzione per reato (mafia vs ordinario vs terrorismo) e tipologia (trojan in particolare). Unico dataset statistico nazionale sulle intercettazioni.
