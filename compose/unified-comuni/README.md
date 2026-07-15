# unified-comuni

Dataset composito multi-fonte per comune italiano. Ogni riga = comune × anno.
Legge i parquet già pubblicati su GCS via HTTPS diretto.

## Schema (44 colonne)

| Blocco | Colonne |
|--------|---------|
| 🔑 Chiave | `codice_istat`, `anno` |
| 📍 Anagrafica | `denominazione`, `sigla_provincia`, `regione`, `superficie_km2`, `altitudine` |
| 👥 Popolazione | `popolazione_residente`, `maschi`, `femmine` |
| 💰 IRPEF | `contribuenti`, `reddito_imponibile_eur`, `reddito_complessivo_eur`, `reddito_procapite`, `reddito_lav_dip_eur`, `reddito_pensione_eur`, `imposta_netta_eur`, `addizionale_comunale_eur`, `addizionale_regionale_eur` |
| 🗑️ Rifiuti | `ru_tonnellate`, `rd_tonnellate`, `rd_pct`, `rd_procapite_kg` |
| 🌍 Consumo suolo | `suolo_consumato_ha`, `suolo_consumato_pct`, `suolo_incremento_ha` |
| 💸 FSC | `popolazione_fsc`, `capacita_fiscale`, `dotazione_finale_fsc`, `fondo_perequativo`, `imu_tasi_standard` |
| 🏛️ SIOPE | `siope_entrate`, `siope_uscite`, `siope_avanzo`, `siope_personale`, `siope_investimenti`, `siope_imposte_proprie`, `siope_fondi_perequativi` |
| 👷 Dipendenti PA | `dipendenti_totali`, `dipendenti_assunti`, `dipendenti_cessati`, `dipendenti_saldo` |
| 📋 PNRR | `pnrr_progetti`, `pnrr_fin_totale` |

## Fonti

| Dataset | Periodo | Chiave di join |
|---------|:-------:|----------------|
| `comuni_master` | 2026 | `codice_istat` |
| `popolazione_istat_comunale` | 2019–2025 | `codice_comune` |
| `irpef_comunale` | 2019–2024 | `codice_istat_comune` |
| `ispra_ru_base` | 2020–2024 | `RIGHT(codice_comune_istat,6)` |
| `ispra_consumo_suolo` | 2024 (long, 11 periodi) | `LPAD(pro_com,6,'0')` |
| `opencivitas_fsc_2025_rso` | 2022–2025 | `UPPER(TRIM(comune)) + regione` |
| `siope_bilancio_unificato` | 2021–2025 | `codice_ente → bdap.codice_ente_siope` |
| `dipendenti_pubblici` | 2019–2023 | `codice_ente_bdap → bdap.id_ente` |
| `pnrr_progetti` | 2026 | `cf_soggetto_attuatore → comune.codice_fiscale` |
| `bdap_anagrafe_enti` (bridge) | 2026 | bridge per SIOPE e dipendenti |

## Copertura

| Anno | Comuni | Pop | IRPEF | Rifiuti | Suolo | FSC | SIOPE | Dipendenti | PNRR |
|:----:|:-----:|:---:|:-----:|:-------:|:-----:|:---:|:-----:|:----------:|:----:|
| 2019 | 7.479 | ✅ | ✅ | — | ✅ | — | — | ✅ | ✅ |
| 2020 | 7.504 | ✅ | ✅ | ✅ | ✅ | — | — | ✅ | ✅ |
| 2021 | 7.507 | ✅ | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ |
| 2022 | 7.510 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 2023 | 7.512 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 2024 | 7.512 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 2025 | 7.516 | ✅ | — | — | — | ✅ | ✅ | — | ✅ |

Note:
- **Suolo**: dataset ISPRA consumo suolo disponibile solo fino al 2024. Anno 2025 = NULL.
- **Dipendenti**: fonte MEF-BDAP arriva al 2024. Anno 2025 = NULL.
- **SIOPE**: fonte parte dal 2021. Anni <2021 = NULL.
- **PNRR**: match via codice fiscale, ~3.700 comuni con progetti intestati direttamente al comune.
- **FSC**: join testuale su denominazione + regione. Copertura ~85% (escluse righe regionali).

## Run

```bash
toolkit run full --config compose/unified-comuni/dataset.yml --years 2026
```
