# Eurostat Economy (compose)

**Dataset**: `eurostat_economy`
**Tipo**: compose — unisce 4 dataset Eurostat NUTS3 in una vista economia regionale

## Cos'è

Vista unificata degli indicatori economici regionali europei: PIL, Valore Aggiunto Lordo (7 settori), occupazione e produttività. Ogni riga = (geo, year) con 26 colonne.

**Copertura**: 2000-2024, tutti i paesi EU/EEA, tutti i livelli NUTS (0-3).

## Schema (26 colonne)

| Gruppo | Colonne |
|---|---|
| Chiave | `geo`, `year`, `nuts_level`, `country_code`, `geo_label_en` |
| PIL | `gdp_per_capita`, `gdp_million_eur`, `gdp_pps_hab` |
| GVA | `gva_total_million`, `gva_industry_million`, `gva_construction_million`, `gva_trade_million`, `gva_ict_million`, `gva_financial_services_million`, `gva_public_admin_million`, `gva_*_pct` (6 colonne %) |
| Occupazione | `employment_thousands`, `nominal_labour_productivity_eur`, `gdp_per_employed_eur` |

## Dataset sorgente

| Dataset | Dataflow | Ruolo |
|---|---|---|
| `eurostat_gdp_nuts3` | NAMA_10R_3GDP | PIL pro-capite, totale, PPS |
| `eurostat_gva_nuts3` | NAMA_10R_3GVA | GVA per settore NACE |
| `eurostat_emp_nuts3` | NAMA_10R_3EMPERS | Occupati (migliaia) |
| `eurostat_labour_productivity_nuts3` | NAMA_10R_3NLP | Produttività nominale |

## Mart

| Mart | Filtro | Righe stimate |
|---|---|---|
| `mart_it_nuts3` | IT NUTS3 (107 province) | ~2.675 |
