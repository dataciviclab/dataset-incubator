# unified-comuni — note tecniche

## Architettura

```
dataset.yml → raw (solo hub da GCS) → clean (S3 glob su GCS) → mart
```

Il clean SQL legge i parquet dei dataset sorgente **direttamente da GCS**
tramite S3 glob pattern (`s3://dataciviclab-clean/.../*/*.parquet`).
Questo significa che:

- Non serve elencare singoli anni o file
- Un nuovo anno pubblicato in una fonte viene preso automaticamente
- L'anno in `dataset.yml` è solo una label per il path di output

## Join keys

Documentate in `registry/join_map.yaml`.

| Fonte | Colonna | Normalizzazione |
|-------|---------|-----------------|
| popolazione | `codice_comune` | direct |
| irpef | `codice_istat_comune` | direct |
| rifiuti | `codice_comune_istat` | `RIGHT(..., 6)` |
| FSC | `comune` | `UPPER(TRIM(...))` |

## Db dipendenze

Richiede httpfs (DuckDB, caricato dal toolkit dal toolkit per tutte
le connessioni clean SQL). Il bug httpfs "Information loss on integer cast"
di DuckDB < 1.5.3 è fixato dalla 1.5.4 (usata nel .venw del workspace).

## Copertura

| Anno | Comuni | Popolazione | IRPEF | Rifiuti | FSC |
|:----:|:-----:|:-----------:|:-----:|:-------:|:---:|
| 2019 | 7.484 | ✅ | ✅ | — | — |
| 2020 | 7.509 | ✅ | ✅ | ✅ | — |
| 2021 | 7.512 | ✅ | ✅ | ✅ | — |
| 2022 | 7.515 | ✅ | ✅ | ✅ | — |
| 2023 | 7.517 | ✅ | ✅ | ✅ | — |
| 2024 | 7.517 | ✅ | ✅ | ✅ | — |
| 2025 | 7.521 | ✅ | — | — | ✅ |

## Aggiungere una nuova fonte

1. Aggiungere una CTE nel clean SQL con `read_parquet('s3://...glob...'`
2. Aggiungere un LEFT JOIN nella SELECT finale
3. Aggiungere la mappatura in `registry/join_map.yaml`

## Run

```bash
toolkit run full --config candidates/unified-comuni/dataset.yml --years 2026
```
