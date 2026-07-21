# penale-flussi

Flussi dei procedimenti penali: iscritti, definiti e pendenti per ufficio giudiziario.

## Dati

- **Fonte**: Ministero della Giustizia — DG Statistica (datiestatistiche.giustizia.it)
- **File**: `PenaleFlussi20142025.xlsx` + `PenaleFlussi20052013.xlsx`
- **Copertura**: 2005–2025 (20+ anni)
- **Uffici**: Cassazione, Corte d'Appello, Tribunale ordinario, Giudice di Pace, Tribunale per i minorenni, Procura Generale, Procura della Repubblica, Procura Minorenni
- **Granularità**: nazionale, distrettuale (26 distretti), circondariale (140 tribunali)
- **Metriche**: iscritti, definiti, pendenti
- **Licenza**: dati pubblici (Italian Open Data License v2.0)

## Join possibili

- `civile_flussi` — stesso schema, confronto civile/penale
- `giustizia_penale_indicatori` — clearance rate e disposition time per gli stessi uffici
- `distretto` → anagrafe distretti giudiziari
