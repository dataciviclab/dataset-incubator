# Note tecniche — eurostat-demography

## Architettura

Compose che legge parquet puliti direttamente da GCS.

1. **Hub**: area_nuts3 × demo_r_pjangrp3 (anni 2014-2025)
2. **4 CTE dominio**: popolazione, densità, struttura età, bilancio
3. **LEFT JOIN** su (geo, year)
4. **WHERE** elimina righe senza alcun dato

## Qualità (run 2026-07-26)

| Metrica | Valore |
|---|---|
| Righe clean EU | 20.949 |
| Colonne | 18 |
| Population non-NULL | 98.1% |
| Pop density non-NULL | 85.9% |
| Median age non-NULL | 0% per IT NUTS3 |
| Natural change non-NULL | 90.2% |
| IT NUTS3 coverage | 107/107 province |

## Perché median_age è NULL per Italia NUTS3

Il dataset Eurostat `pop_structure_nuts3` (DEMO_R_PJANIND3) per l'Italia pubblica 51 indicatori (OLDDEP1, PC_Y0_14, DEPRATIO1, ...) ma non MEDAGEPOP (età mediana), PC_Y65 e PC_Y75. Questi sono disponibili solo a NUTS2. La limitazione è della fonte, non del compose.

## Fonte popolazione

A differenza del dataset `pop_nuts3` (che ha popolazione solo a NUTS2 per IT), il compose usa `demo_r_pjangrp3` che ha copertura NUTS3 completa per l'Italia (107 province). Range: 2014-2025.
