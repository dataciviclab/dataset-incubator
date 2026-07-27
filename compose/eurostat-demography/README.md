# Eurostat Demography (compose)

**Dataset**: `eurostat_demography`
**Tipo**: compose — unisce 4 dataset Eurostat in una vista demografica regionale

## Cos'è

Vista unificata degli indicatori demografici regionali europei: popolazione, densità, struttura per età, bilancio demografico. Ogni riga = (geo, year) con 18 colonne.

**Copertura**: 2014-2025, tutti i paesi EU/EEA, tutti i livelli NUTS (0-3).

## Schema (18 colonne)

| Gruppo | Colonne |
|---|---|
| Chiave | `geo`, `year`, `nuts_level`, `country_code`, `geo_label_en` |
| Popolazione | `population`, `pop_density_km2` |
| Struttura età | `median_age`, `old_age_dependency_pct`, `youth_pct`, `total_dependency_pct`, `over65_pct`, `over75_pct` |
| Bilancio | `natural_change`, `net_migration`, `total_change` |

## Dataset sorgente

| Dataset | Dataflow | Ruolo |
|---|---|---|
| `eurostat_demo_r_pjangrp3_nuts3` | DEMO_R_PJANGRP3 | Popolazione per età e sesso (NUTS3) |
| `eurostat_pop_density_nuts3` | DEMO_R_D3DENS | Densità abitativa |
| `eurostat_pop_structure_nuts3` | DEMO_R_PJANIND3 | Indicatori struttura età |
| `eurostat_demo_balance_nuts3` | DEMO_R_GIND3 | Bilancio demografico |

## Mart

| Mart | Filtro | Righe stimate |
|---|---|---|
| `mart_it_nuts3` | IT NUTS3 (107 province) | ~1.284 |

## Limitazioni note

- `median_age`, `over65_pct`, `over75_pct` sono NULL per l'Italia NUTS3 (Eurostat pubblica questi indicatori solo a livello NUTS2 per IT)
