# anac-collaudo — Note tecniche

## Intake

Fonte ANAC su dati.gov.it. CKAN con resource_name "collaudo_csv" + extractor unzip_first_csv.
**WAF**: l'API diretta di dati.anticorruzione.it blocca la risorsa "collaudo" (nome triggerante).
Usare portal_url dati.gov.it.

## Qualità (run 2026-07-25)

| Metrica | Valore |
|---|---|
| Righe | 648.862 |
| CIG distinti | 648.674 |
| Collaudi positivi | ~98,6% |
| Collaudi negativi | ~1,4% |
| CIG nulli | 0 ✅ |

## Join

- `cig` + `id_aggiudicazione` → `anac_aggiudicazioni`
- Chiude il ciclo: bando → aggiudicazione → SAL → collaudo
