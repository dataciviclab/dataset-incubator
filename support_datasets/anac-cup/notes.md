# anac-cup — Note tecniche

## Intake

Fonte ANAC su dati.gov.it. CKAN con resource_name "cup_csv" + extractor unzip_first_csv.
WAF ANAC: usare portal_url dati.gov.it invece di dati.anticorruzione.it.

## Qualità (run 2026-07-25)

| Metrica | Valore |
|---|---|
| Righe | 7.124.007 |
| CIG distinti | 7.004.949 |
| CUP distinti | 1.538.176 |
| CIG per CUP (media) | 4,6 |
| CIG / CUP nulli | 0 ✅ |

## Join

- `cig` → `anac_bandi_gara`, `anac_aggiudicazioni`, `anac_aggiudicatari`, `anac_subappalti`
- `cup` → `pnrr_progetti`, `mit_opere_incompiute_2020`, OpenCUP progetti, BDAP MOP
