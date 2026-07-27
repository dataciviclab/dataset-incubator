# Eurostat Territory (compose)

**Dataset**: `eurostat_territory`
**Tipo**: compose — unisce 4 dataset Eurostat NUTS3 in una vista territoriale

## Cos'è

Vista unificata degli indicatori territoriali regionali europei: superficie, turismo, criminalità, incidenti stradali. Ogni riga = (geo, year) con 11 colonne.

**Copertura**: 2000-2024, paesi EU/EEA con dati disponibili, tutti i livelli NUTS (0-3).

## Schema (11 colonne)

| Gruppo | Colonne |
|---|---|
| Chiave | `geo`, `year`, `nuts_level`, `country_code`, `geo_label_en` |
| Territorio | `area_km2` |
| Turismo | `total_nights_spent` |
| Criminalità | `total_crimes` |
| Trasporti | `road_accidents` |

## Dataset sorgente

| Dataset | Dataflow | Ruolo |
|---|---|---|
| `eurostat_area_nuts3` | REG_AREA3 | Superficie territoriale (km²) |
| `eurostat_tourism_nuts3` | TOUR_OCC_NIN2 | Pernottamenti turistici |
| `eurostat_crime_nuts3` | CRIM_GEN_REG | Reati registrati |
| `eurostat_tran_sf_roadnu` | TRAN_SF_ROADNU | Incidenti stradali |

## Mart

| Mart | Filtro | Righe stimate |
|---|---|---|
| `mart_it_nuts3` | IT NUTS3 (107 province) | ~2.675 |

## Limitazioni note

- I dataset hanno copertura EU parziale: area_km2 disponibile dal 2013, turismo non copre tutte le regioni, criminalità non UE-wide
