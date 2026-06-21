# unified-comuni

Dataset composito multi-fonte per comune italiano. Ogni riga = comune × anno.
Legge i parquet già pubblicati su GCS via S3 glob (nessuna lista da mantenere).

## Schema (30 colonne)

| Blocco | Colonne |
|--------|---------|
| 🔑 Chiave | `codice_istat`, `anno` |
| 📍 Anagrafica | `denominazione`, `sigla_provincia`, `regione`, `superficie_km2`, `altitudine` |
| 👥 Popolazione | `popolazione_residente`, `maschi`, `femmine` |
| 💰 IRPEF | `contribuenti`, `reddito_imponibile_eur`, `reddito_complessivo_eur`, `reddito_procapite`, `reddito_lav_dip_eur`, `reddito_pensione_eur`, `imposta_netta_eur`, `addizionale_comunale_eur`, `addizionale_regionale_eur` |
| 🗑️ Rifiuti | `ru_tonnellate`, `rd_tonnellate`, `rd_pct`, `rd_procapite_kg` |
| 🌍 Consumo suolo | `suolo_consumato_ha`, `suolo_consumato_pct`, `suolo_incremento_ha` |
| 💸 FSC | `popolazione_fsc`, `capacita_fiscale`, `dotazione_finale_fsc`, `fondo_perequativo`, `imu_tasi_standard` |

## Fonti

| Dataset | Periodo | Chiave |
|---------|:-------:|--------|
| `comuni_master` | 2026 | `codice_istat` |
| `popolazione_istat_comunale` | 2019–2025 | `codice_comune` |
| `irpef_comunale` | 2019–2024 | `codice_istat_comune` |
| `ispra_ru_base` | 2020–2024 | `RIGHT(codice_comune_istat,6)` |
| `ispra_consumo_suolo` | 2024 | `LPAD(pro_com,6,'0')` |
| `opencivitas_fsc_2025_rso` | 2025 | `UPPER(TRIM(comune))` |

## Copertura

| Anno | Comuni | Pop | IRPEF | Rifiuti | Suolo | FSC |
|:----:|:-----:|:---:|:-----:|:-------:|:-----:|:---:|
| 2019 | 7.484 | ✅ | ✅ | — | ✅ | ✅ |
| 2020 | 7.509 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 2021 | 7.512 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 2022 | 7.515 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 2023 | 7.517 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 2024 | 7.517 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 2025 | 7.521 | ✅ | — | — | ✅ | ✅ |

## Run

```bash
toolkit run full --config candidates/unified-comuni/dataset.yml --years 2026
```
