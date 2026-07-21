# monitoraggio-mensile-civile

Monitoraggio mensile dei tribunali: iscritti e definiti civili per mese, sede e materia.

## Dati

- **Fonte**: Ministero della Giustizia — DG Statistica (datiestatistiche.giustizia.it)
- **File**: `Monitoraggio_mensile.xlsx`, sheet "DATA"
- **Copertura**: 2019–2025 (dati mensili)
- **Granularità**: sede/mese — 26 distretti, 5 macro-aree (Nord, Centro, Sud, Isole)
- **Materie**: Affari contenziosi, Lavoro, Previdenza, Procedimenti speciali sommari, Volontaria giurisdizione
- **Metriche**: iscritti, definiti (con flag consolidati/provvisori)
- **Righe**: 139.113
- **Run**: `toolkit run all --config candidates/monitoraggio-mensile-civile/dataset.yml --years 2025` ✅
- **Licenza**: dati pubblici (Italian Open Data License v2.0)

## Join possibili

- `civile_flussi` — confronto mensile vs annuale sugli stessi uffici
- `distretto` → anagrafe distretti giudiziari

## Valore

Unico dataset mensile del portale. Permette analisi di stagionalità, trend infra-annuali e monitoraggio congiunturale.
