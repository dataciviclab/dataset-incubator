# anac-stati-avanzamento — Note tecniche

## Intake

Fonte ANAC su dati.gov.it. CKAN con resource_name "stati-avanzamento_csv" + extractor unzip_first_csv.
WAF ANAC: usare portal_url dati.gov.it.

## Qualità (run 2026-07-25)

| Metrica | Valore |
|---|---|
| Righe | 1.274.801 |
| CIG distinti | 343.824 |
| SAL in linea | ~96,9% |
| SAL in ritardo | ~2,6% |
| SAL in anticipo | ~0,5% |
| SAL per CIG (media) | 3,7 |
| CIG nulli | 0 ✅ |

## Join

- `cig` + `id_aggiudicazione` → `anac_aggiudicazioni`
- Completa il ciclo: bando → aggiudicazione → SAL → collaudo
