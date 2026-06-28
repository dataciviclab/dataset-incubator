# Notes — mef-rappresentanti-partecipate

## Stato

Candidate v0. Run passato su 2017-2023 (7 anni, schema uniforme).

## Anni

| Anno | Righe | Note |
|:----:|:-----:|------|
| 2017 | 17.911 | |
| 2018 | 16.610 | |
| 2019 | 16.930 | |
| 2020 | 16.712 | |
| 2021 | 17.192 | |
| 2022 | 17.305 | URL con .CSV maiuscolo |
| 2023 | 16.785 | |

## Anni esclusi

- **2014**: disponibile come `OpenData_2014_Incarichi_CSV.csv` con schema diverso
- **2015-2016**: disponibili ma con nomi colonna diversi (es. `Sede Amministrazione Regione` vs `Amministrazione Regione Sede`, `Rappresentante Codice Fiscale` vs `Rappresentante identificativo`)

## URL pattern

| Anni | Pattern |
|------|---------|
| 2017-2021, 2023 | `/partecipazioni_{ANNO}/dati_rappresentanti_anno_{ANNO}.csv` |
| 2022 | `/2022/dati_rappresentanti_anno_2022.CSV` |

## Join

Joinabile con `dait_amministratori_locali` via nome e cognome del rappresentante (join testuale).
