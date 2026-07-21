# Giustizia penale — clearance rate e disposition time

## Domanda

Dove il sistema penale smaltisce meglio e dove invece i procedimenti restano più a lungo in carico?

Il clearance rate (rapporto tra definiti e iscritti) e il disposition time (tempo medio di definizione in giorni) permettono di confrontare l'efficienza del sistema tra distretti e tipologie di ufficio.

## Fonte

- **Ente**: Ministero della Giustizia — Direzione Generale di Statistica e Analisi Organizzativa
- **URL**: https://datiestatistiche.giustizia.it/page/it/clearance-rate-e-disposition-time-penale
- **File**: https://datiestatistiche.giustizia.it/cmsresources/cms/documents/Indicatori_Penali.xlsx

## Perimetro

4 sheet unificati: **Tribunali**, **Corti d'Appello**, **Giudici di Pace**, **Tribunale per i Minorenni**.
Serie completa 2014–2025.

## Schema

| Colonna | Tipo | Descrizione |
|---------|------|-------------|
| anno | INTEGER | Anno di riferimento |
| tipo_ufficio | VARCHAR | Tipo ufficio (Tribunale, Corte d'Appello, Giudice di Pace, Minorenni) |
| distretto | VARCHAR | Distretto di corte d'appello |
| sede | VARCHAR | Comune della sede |
| sezione | VARCHAR | Tipologia sezione (Dibattimento, GIP/GUP, ecc.) |
| clearance_rate | DOUBLE | Rapporto definiti/iscritti (1 = equilibrio) |
| disposition_time_gg | DOUBLE | Tempo medio di definizione in giorni |

## Output

Mart aggregato per anno / distretto / tipo_ufficio con medie, min, max.

## Stato

- incubating (update: 4 sheet unificati, anni 2014–2025)

## Prossimo passo

PR → merge → post-merge push GCS
