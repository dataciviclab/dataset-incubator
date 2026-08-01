# Notes — anpr-mobilita-residenziale

## Stato

Candidate a standard v1 (2026-08-01): mart analitiche serie (saldi / corridoi /
trend mensile). Run passed con years: [2026]. 22.176 righe, 7 colonne.

## Copertura per anno

| Anno | Righe | Note |
|:----:|:-----:|------|
| 2022 | 3.844 | Apr-Dic (subentro ANPR parziale) |
| 2023 | 5.116 | Completo |
| 2024 | 5.120 | Completo |
| 2025 | 5.118 | Completo |
| 2026 | 2.552 | Gen-Giu (dati parziali) |

## Note tecniche

- Fonte: http_file standard (GitHub raw, ANPR opendata)
- clean.sql: macro standard (cast_int, normalize_string, LPAD codici ISTAT)
- Il dataset è un file unico con tutti gli anni: le mart leggono `FROM clean_input`
  (nessun multi-year necessario — i 5 anni sono nello stesso parquet)
- ESTERO è una entità valida (arrivo e partenza) — non filtrata
- primary_key clean: [anno, mese, partenza, arrivo]

## Decisioni metodologiche (2026-08-01)

- Mart pass-through rimosso: il dato grezzo è una matrice origine→destinazione;
  le 3 mart serie rispondono alle 13 domande della discussion #393
- `quota_interni_pct` in mart_saldi: flussi interni / (arrivi + partenze - interni)
  — misura l'autosufficienza regionale (D4)
- I saldi cumulati multi-anno non coincidono coi saldi di un singolo anno
  citati nella discussion (es. Lombardia cumulato +80.6k vs +81.4k 2025):
  differenza attesa, sono metriche diverse

## Saldi netti interregionali 2025 (escluso ESTERO)

| Regione | Uscite | Entrate | Saldo |
|---------|:------:|:-------:|:----:|
| Campania | 45.417 | 24.603 | -20.814 |
| Sicilia | 34.765 | 21.505 | -13.260 |
| Puglia | 28.295 | 19.723 | -8.572 |
| Calabria | 20.113 | 12.583 | -7.530 |
| … | … | … | … |
