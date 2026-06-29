# Notes — anpr-mobilita-residenziale

## Stato

Candidate v0. Run passato con years: [2026]. 21.750 righe, 7 colonne.

## Copertura per anno

| Anno | Righe | Note |
|:----:|:-----:|------|
| 2022 | 3.844 | Apr-Dic (subentro ANPR parziale) |
| 2023 | 5.116 | Completo |
| 2024 | 5.120 | Completo |
| 2025 | 5.118 | Completo |
| 2026 | 2.552 | Gen-Giu (dati parziali) |

## Saldi netti interregionali 2025 (escluso ESTERO)

| Regione | Uscite | Entrate | Saldo |
|---------|:------:|:-------:|:----:|
| Campania | 45.417 | 24.603 | -20.814 |
| Sicilia | 34.765 | 21.505 | -13.260 |
| Puglia | 28.295 | 19.723 | -8.572 |
| Calabria | 20.113 | 12.583 | -7.530 |
| … | … | … | … |
| Lombardia | 63.203 | 77.870 | **+14.667** |
| Emilia Romagna | 33.750 | 44.646 | **+10.896** |

## Fonte

Repo GitHub ufficiale: `italia/anpr-opendata`
File: `data/cambi_residenza.csv` — aggiornato automaticamente via GitHub Actions.

## Note

- Dato aggiornato quasi in tempo reale (ANPR, non ISTAT con 2 anni di ritardo)
- Subentro ANPR parziale nel 2022: possibile sottostima comuni minori del Sud
- Include flussi con ESTERO (cancellazioni/iscrizioni anagrafiche)
- Il file è unico e contiene tutta la serie storica
