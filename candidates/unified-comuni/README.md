# unified-comuni

**Dataset composito** che unisce popolazione, redditi, rifiuti, consumo suolo
e Fondo di Solidarietà Comunale per comune italiano.

Ogni riga = comune × anno. Non ha fonti primarie: **legge i parquet clean
dei candidati dataset già pubblicati su GCS** e li JOINa via `comuni_master`.

## Fonti incluse

| Dominio | Dataset | Colonna chiave | Periodo |
|---------|---------|----------------|:-------:|
| 🏛️ Hub anagrafico | `comuni_master` | `codice_istat` | 2026 |
| 👥 Popolazione | `popolazione_istat_comunale` | `codice_comune` | 2019–2025 |
| 💰 Redditi | `irpef_comunale` | `codice_istat_comune` | 2019–2024 |
| 🗑️ Rifiuti | `ispra_ru_base` | `RIGHT(codice_comune_istat,6)` | 2020–2024 |
| 🌍 Consumo suolo | `ispra_consumo_suolo` | `LPAD(pro_com,6,'0')` | 2024 |
| 💸 FSC | `opencivitas_fsc_2025_rso` | `UPPER(TRIM(comune))` | 2025 |

## Schema (32 colonne)

```
codice_istat, anno, denominazione, sigla_provincia, provincia, regione
superficie_km2, altitudine
popolazione_residente, maschi, femmine
numero_contribuenti
reddito_imponibile_eur, reddito_complessivo_eur, reddito_procapite
reddito_lav_dip_eur, reddito_da_pensione_eur, imposta_netta_eur
addizionale_comunale_eur, addizionale_regionale_eur
totale_ru_tonnellate, totale_rd_tonnellate, percentuale_rd, rd_procapite_kg
suolo_consumato_ha, suolo_consumato_pct, suolo_incremento_netto_ha
popolazione_fsc, capacita_fiscale, dotazione_finale_fsc
fondo_perequativo, imu_tasi_standard
```

## Join Map

Tutte le chiavi di join sono documentate in `registry/join_map.yaml`.
Hub centrale: `comuni_master` (`codice_istat` 6 cifre).

## Dipendenze

- toolkit **>= 1.39.0** (richiede httpfs per S3 glob patterns)
- Dataset elencati in "Fonti incluse" devono essere pubblicati su GCS

## Run

```bash
toolkit run full --config candidates/unified-comuni/dataset.yml --years 2024
```
