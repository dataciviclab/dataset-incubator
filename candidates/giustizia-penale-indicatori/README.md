# Giustizia penale — clearance rate e disposition time

## Domanda

Dove il sistema penale smaltisce meglio e dove invece i procedimenti restano più a lungo in carico?

Il clearance rate (rapporto tra definiti e iscritti) e il disposition time (tempo medio di definizione in giorni) permettono di confrontare l'efficienza del sistema tra distretti e tipologie di ufficio.

## Fonte

- **Ente**: Ministero della Giustizia — Direzione Generale di Statistica e Analisi Organizzativa
- **URL**: https://datiestatistiche.giustizia.it/page/it/clearance-rate-e-disposition-time-penale
- **File**: https://datiestatistiche.giustizia.it/cmsresources/cms/documents/Indicatori_Penali.xlsx
- **Licenza**: dati pubblici (Italian Open Data License v2.0)

## Perimetro

4 sheet unificati via script `scripts/unite_sheets_penali.py`:
| Sheet | Righe |
|---|---|
| Tribunali | 5.039 |
| Corti d'Appello | 1.037 |
| Giudici di Pace | 3.359 |
| Tribunale per i Minorenni | 1.043 |
| **Totale** | **10.478** |

Serie completa 2014–2025.

## Schema

| Colonna | Tipo | Descrizione |
|---------|------|-------------|
| anno | INTEGER | Anno di riferimento |
| tipo_ufficio | VARCHAR | Tipo ufficio (Tribunale, Corte d'appello, Giudice di pace, Tribunale per i minorenni) |
| distretto | VARCHAR | Distretto di corte d'appello |
| sede | VARCHAR | Comune della sede |
| sezione | VARCHAR | Tipologia sezione (Dibattimento, GIP/GUP, ecc.) |
| clearance_rate | DOUBLE | Rapporto definiti/iscritti (1 = equilibrio) |
| disposition_time_gg | DOUBLE | Tempo medio di definizione in giorni |

## Output

Mart aggregato per anno / distretto / tipo_ufficio con medie, min, max.

## Run

```bash
TOOLKIT_ALLOW_SCRIPT_SOURCE=1 toolkit run all --config candidates/giustizia-penale-indicatori/dataset.yml --years 2025
```

La variabile `TOOLKIT_ALLOW_SCRIPT_SOURCE=1` è necessaria per abilitare lo script Python che scarica e unisce i 4 sheet XLSX.

## Stato

- incubating (update #693: 4 sheet unificati, 10.478 righe, 2014–2025)

## Prossimo passo

PR → merge → post-merge push GCS
