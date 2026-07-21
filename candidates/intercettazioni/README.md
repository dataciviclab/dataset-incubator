# intercettazioni

Bersagli intercettazioni per tipologia, reato e distretto.

## Dati

- **Fonte**: Ministero della Giustizia — DG Statistica (datiestatistiche.giustizia.it)
- **File**: `Intercettazioni.xlsx`
- **Copertura**: 2014–2025 (+ anni isolati 1994, 2011)
- **Sheet**:
  - **Tutti gli uffici** (v0): anno, tipo ufficio, distretto, tipologia intercettazione, n. bersagli
  - **Tipologia di reato** (v1): aggiunge tipo di reato (ordinaria, DDA/mafia, terrorismo)
- **Tipologie intercettazione**: Telefoniche, Ambientali, Informatiche, Trojan
- **Granularità**: distrettuale (26 distretti)
- **Righe**: ~7.5K totali
- **Licenza**: dati pubblici (Italian Open Data License v2.0)

## Join possibili

- `distretto` → anagrafe distretti giudiziari

## Valore

Tema di forte interesse pubblico. Distinzione per reato (mafia vs ordinario vs terrorismo) e tipologia (trojan in particolare). Unico dataset statistico nazionale sulle intercettazioni.
