# unified-comuni — note tecniche

## Cos'è

Dataset composito che unisce popolazione, redditi, rifiuti, consumo suolo e FSC
per comune italiano. Ogni riga = comune × anno.

Non ha fonti primarie: **legge i parquet clean già pubblicati su GCS** e li
JOINa via `comuni_master` come hub centrale.

## Architettura

```
comuni_master (hub) ──┐
popolazione_istat   ──┤
irpef_comunale      ──┤──> JOIN su codice ISTAT ──> unified_comuni
ispra_ru_base       ──┤
ispra_consumo_suolo ──┤
opencivitas_fsc     ──┘
```

## Join keys

Ogni fonte ha la sua normalizzazione (documentata in `registry/join_map.yaml`):

| Fonte | Colonna | Formato | Normalizzazione |
|-------|---------|---------|-----------------|
| popolazione | `codice_comune` | istat_6 | direct |
| irpef | `codice_istat_comune` | istat_6 | direct |
| rifiuti | `codice_comune_istat` | istat_8 | `RIGHT(..., 6)` |
| consumo suolo | `pro_com` | istat_5 | `LPAD(..., 6, '0')` |
| FSC | `comune` | denominazione | `UPPER(TRIM(...))` |

## Anni

| Fonte | Copertura | Anno usato | Note |
|-------|:---------:|:----------:|------|
| hub (comuni_master) | 2026 | 2026 | Golden record |
| popolazione | 2019-2025 | {year} | Serie multi-anno |
| irpef | 2019-2024 | {year} | Dati 2024 aggiunti in PR #532 |
| rifiuti | 2020-2024 | {year} | Serie multi-anno |
| consumo suolo | 2024 | 2024 | Snapshot |
| FSC | 2025 | 2025 | Singolo anno |

`{year}` è risolto dal toolkit in base al valore configurato in `dataset.yml`.

## Run

```bash
toolkit run full --config candidates/unified-comuni/dataset.yml --years 2024
toolkit run full --config candidates/unified-comuni/dataset.yml --years 2023
```

## Stato (2026-06-21)

| Anno | Righe | Popolazione | IRPEF | Rifiuti | Cons. suolo | FSC | Validazione |
|:----:|:-----:|:-----------:|:-----:|:-------:|:-----------:|:---:|:-----------:|
| 2023 | 7.517 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ passata |
| 2024 | 7.517 | ✅ | ✅ (da IRPEF 2024) | ✅ | ✅ | ✅ | ✅ passata |

Cross-validato su Abbiategrasso: ogni valore unificato matcha le fonti originali.
- Popolazione 2023: 32.492 (raw) → 32.492 (unified) ✅
- IRPEF 2023: €642.398.192 → €642.398.192 ✅
- IRPEF 2024: €631.383.270 → €631.383.270 ✅ (da PR #532)
- Reddito procapite 2023: 19.771 (calcolato) ✅
- RD% 2023: 71,39% → 71,39% ✅

## Aggiungere una nuova fonte

1. Aggiungere un `http_file` source in `dataset.yml`
2. Aggiungere una CTE e un LEFT JOIN in `sql/clean.sql`
3. Aggiungere la mappatura in `registry/join_map.yaml`
4. (Opzionale) Aggiungere colonna al mart

## Prerequisiti

I dataset sorgente devono esistere su GCS (pubblicati da candidate/support esistenti).
Nessuna dipendenza di esecuzione — il compose non runna i candidati upstream.
