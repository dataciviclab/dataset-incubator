# Notes — mef-rappresentanti-partecipate

## Stato

Candidate v0. Run passato su 2018-2023 (6 anni, schema uniforme).

## Anni

| Anno | Righe | Note |
|:----:|:-----:|------|
| 2018 | 16.610 | |
| 2019 | 16.930 | |
| 2020 | 16.712 | |
| 2021 | 17.192 | |
| 2022 | 17.305 | URL con .CSV maiuscolo |
| 2023 | 16.785 | |

## Anni esclusi

- **2017**: dati importo anomali (100M€ per Formez PA). Escluso.
- **2014**: disponibile come `OpenData_2014_Incarichi_CSV.csv` con schema diverso
- **2015-2016**: disponibili ma con nomi colonna diversi

## URL pattern

| Anni | Pattern |
|------|---------|
| 2017-2021, 2023 | `/partecipazioni_{ANNO}/dati_rappresentanti_anno_{ANNO}.csv` |
| 2022 | `/2022/dati_rappresentanti_anno_2022.CSV` |

## Join

Joinabile con `dait_amministratori_locali` via nome e cognome del rappresentante (join testuale).

## 2026-08-03 — standard v1, mart serie (discussion #406)

### Mart (rimpiazzano mart_rappresentanti pass-through)
- `mart_trend_anno` (multi-year): incarichi, rappresentanti, spesa totale,
  quota gratuiti, riversato, delta/variazione spesa — D1
- `mart_sintesi_incarico`: per (anno, tipo incarico): n remunerati, importo
  medio/max, spesa — D2 (AD vs consigliere), D11 (liquidatori)
- `mart_gender_gap`: per (anno, genere): n remunerati, importo medio, spesa —
  D3 (divario di genere)
- `mart_top_amministrazioni`: per (anno, amm): n incarichi, rappresentanti,
  spesa, riversato, quota gratuiti — D5 (chi nomina), D8 (riversamento)

### Fix clean.sql
- trim/try_cast/REPLACE manuale → macro standard: normalize_string (28x),
  cast_int, cast_bigint, normalize_italian_number (importi italiani)
- required_columns completo (29, mancavano societa_anno_costituzione,
  incarico_importo_eur, incarico_riversato_eur)
- primary_key [anno, rapp_id, societa_cf, amm_cf, incarico_tipo,
  incarico_data_inizio] — 0 duplicati verificati

### Numeri chiave (combaciano con discussion #406)
- Spesa PA: 109,7M → 132,9M (2018→2023, +21%)
- Gender gap 2023: F €12.690 vs M €18.679 (68%) — discussion cita 65% (media 6 anni)
- AD €63.923 medio (6x consigliere), liquidatori €24.850
- Top spesa 2023: MEF €5,5M, Roma €4,6M, Milano €3,8M
