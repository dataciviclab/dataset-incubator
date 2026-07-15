# unified-comuni — note tecniche

## Architettura

```
dataset.yml → raw (solo hub da GCS) → clean (HTTPS diretto su GCS) → mart
```

Il clean SQL legge i parquet dei dataset sorgente **direttamente da GCS**
tramite HTTPS (`read_parquet([URL...], union_by_name=true)`).
I path sono espliciti per anno (nessun glob pattern).

L'anno in `dataset.yml` è solo una label per il path di output.
Il compose produce un unico file multi-anno.

## Join keys

Documentate anche in `registry/join_map.yaml`.

| Fonte | Colonna | Normalizzazione | Bridge |
|-------|---------|-----------------|--------|
| popolazione | `codice_comune` | direct | — |
| irpef | `codice_istat_comune` | direct | — |
| rifiuti | `codice_comune_istat` | `RIGHT(..., 6)` | — |
| consumo suolo | `pro_com` | `LPAD(..., 6, '0')` | — |
| FSC | `comune` | `UPPER(TRIM(...)) + regione` | — |
| SIOPE | `codice_ente` | via `bdap.codice_ente_siope` | bdap_anagrafe_enti |
| dipendenti | `codice_ente_bdap` | via `bdap.id_ente` | bdap_anagrafe_enti |
| PNRR | `cf_soggetto_attuatore` | `→ comune.codice_fiscale` | — |

### Join testuali (FSC)

`opencivitas_fsc_2025_rso` non ha codice ISTAT comune. Il join è su
`UPPER(TRIM(denominazione)) + regione`. Fragile per:
- Fusioni di comuni (es. nuovi comuni nati da fusione)
- Omonimie (stesso nome in regioni diverse)
- Accenti / caratteri speciali

Cross-validato con `regione` per ridurre i falsi positivi.

## Copertura

| Anno | Comuni | Popolazione | IRPEF | Rifiuti | Suolo | FSC | SIOPE | Dipendenti | PNRR |
|:----:|:-----:|:-----------:|:-----:|:-------:|:-----:|:---:|:-----:|:----------:|:----:|
| 2019 | 7.479 | ✅ | ✅ | — | ✅ | — | — | ✅ | ✅ |
| 2020 | 7.504 | ✅ | ✅ | ✅ | ✅ | — | — | ✅ | ✅ |
| 2021 | 7.507 | ✅ | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ |
| 2022 | 7.511 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 2023 | 7.513 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 2024 | 7.513 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | ✅ |
| 2025 | 7.517 | ✅ | — | — | ✅ | ✅ | ✅ | — | ✅ |

- Dipendenti: fonte MEF-BDAP arriva al 2023. Anni successivi NULL.
- SIOPE: fonte parte dal 2021. Anni precedenti NULL.
- PNRR: match solo via CF (~3.700 comuni su 7.500).

## Aggiungere una nuova fonte

1. Aggiungere una CTE nel clean SQL con `read_parquet('https://...')`
2. Aggiungere un LEFT JOIN nella SELECT finale
3. Aggiornare `registry/join_map.yaml` con la mappatura
4. Aggiornare README.md e notes.md

## Run

```bash
toolkit run full --config compose/unified-comuni/dataset.yml --years 2026
```
