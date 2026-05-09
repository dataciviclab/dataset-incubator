# Giustizia penale — clearance rate e disposition time

## Domanda

Dove il sistema penale smaltisce meglio e dove invece i procedimenti restano più a lungo in carico?

Il clearance rate (rapporto tra definiti e iscritti) e il disposition time (tempo medio di definizione in giorni) permettono di confrontare l'efficienza del sistema tra distretti e tipologie di ufficio.

## Fonte

- **Ente**: Ministero della Giustizia — Direzione Generale di Statistica e Analisi Organizzativa
- **URL**: https://datiestatistiche.giustizia.it/page/it/clearance-rate-e-disposition-time-penale
- **File**: https://datiestatistiche.giustizia.it/cmsresources/cms/documents/Indicatori_Penali_1.xlsx

## Perimetro

Sheet "Tribunali" — Tribunali Ordinari, anni 2014–2024.

Il file XLSX contiene 4 sheet (Tribunali, Corti d'Appello, Giudici di Pace, Tribunale per i Minorenni). Questo candidate copre solo il sheet Tribunali come v0.

## Schema

| Colonna | Tipo | Descrizione |
|---------|------|-------------|
| anno | INTEGER | Anno di riferimento |
| tipo_ufficio | VARCHAR | "Tribunale" |
| distretto | VARCHAR | Distretto di corte d'appello |
| sede | VARCHAR | Comune della sede |
| sezione | VARCHAR | Tipologia sezione (Dibattimento, GIP/GUP, ecc.) |
| clearance_rate | DOUBLE | Rapporto definiti/iscritti (1 = equilibrio) |
| disposition_time_gg | DOUBLE | Tempo medio di definizione in giorni |

## Output

Mart aggregato per anno / distretto / tipo_ufficio con medie, min, max.

## Stato

- incubating

## Prossimo passo

PR → merge → post-merge push GCS