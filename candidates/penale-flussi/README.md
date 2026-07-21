# penale-flussi

Flussi dei procedimenti penali: iscritti (sopravvenuti), definiti e pendenti per ufficio giudiziario.

## Dati

- **Fonte**: Ministero della Giustizia — DG Statistica (datiestatistiche.giustizia.it)
- **File**: `PenaleFlussi20142025.xlsx` (v0), sheet "Data"
- **Copertura**: 2014–2025
- **Uffici**: Cassazione, Corte d'Appello, Tribunale ordinario, Giudice di Pace, Tribunale per i minorenni, Procura Generale, Procura della Repubblica, Procura Minorenni
- **Granularità**: nazionale, distrettuale (26 distretti), circondariale (140 sedi)
- **Metriche**: sopravvenuti (iscritti), definiti, pendenti finali
- **Righe**: ~17.650
- **Licenza**: dati pubblici (Italian Open Data License v2.0)

## Join possibili

- `civile_flussi` — stesso schema (fonte, tipo_ufficio, distretto, sede, anno), confronto civile/penale
- `giustizia_penale_indicatori` — clearance rate e disposition time per gli stessi uffici
- `distretto` → anagrafe distretti giudiziari
