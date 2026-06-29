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

| Regione | Saldo |
|---------|:-----:|
| Campania | -20.814 |
| Sicilia | -13.260 |
| Calabria | -7.530 |
| Puglia | -7.521 |
| Lazio | +3.079 |
| Lombardia | +2.482 |

## Fonte

Repo GitHub ufficiale: `italia/anpr-opendata`
File: `data/cambi_residenza.csv` — aggiornato automaticamente via GitHub Actions.

## Note

- Dato aggiornato quasi in tempo reale (ANPR, non ISTAT con 2 anni di ritardo)
- Subentro ANPR parziale nel 2022: possibile sottostima comuni minori del Sud
- Include flussi con ESTERO (cancellazioni/iscrizioni anagrafiche)
- Il file è unico e contiene tutta la serie storica
