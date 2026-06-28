# Notes — mim-scuola-infanzia

## Stato

Candidate v0. Run passato su tutti gli anni (2018-2025).

## Dati

- Fonte: `INFANZIASTRACITSTA` su dati.istruzione.it
- 4 colonne raw: ANNOSCOLASTICO, CODICESCUOLA, BAMBINICITTADINANZAITALIANA, BAMBINICITTADINANZANONITALIANA
- Arricchito con anagrafica scuole (support `mim-anagrafica-scuole-statali`) via JOIN su codice_scuola
- 14 colonne output con territorio (regione, provincia, comune)

## Anni

| Anno | Anno scolastico | Righe |
|:----:|:---------------:|:-----:|
| 2018 | 2017/2018 | 13.141 |
| 2019 | 2018/2019 | ~13.100 |
| 2020 | 2019/2020 | ~13.000 |
| 2021 | 2020/2021 | ~13.000 |
| 2022 | 2021/2022 | ~13.000 |
| 2023 | 2022/2023 | ~13.000 |
| 2024 | 2023/2024 | ~13.000 |
| 2025 | 2024/2025 | 13.027 |

Il 2017 non è disponibile (server restituisce HTML).

## JOIN

LEFT JOIN con `mim_anagrafica_scuole_statali` su `codice_scuola`. Circa il 2% delle scuole non matcha (scuole non statali o chiuse).

## Pattern URL

```
INFANZIASTRACITSTA{aa}{aa+1}{gg}{mm}{aa}.csv
es. INFANZIASTRACITSTA20242520250831.csv
```
