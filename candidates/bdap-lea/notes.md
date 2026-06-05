# BDAP LEA — Note

## Schema drift: colonna "Oneri Finanziari"

La colonna "Oneri Finanziari" è presente solo in alcuni anni della serie BDAP LEA:

| Anno | Oneri Finanziari |
|:----:|:----------------:|
| 2019 | ✅ presente |
| 2020 | ❌ assente |
| 2021 | ✅ presente |
| 2022 | ✅ presente |
| 2023 | ❌ assente |
| 2024 | ✅ presente |

Gli anni 2012-2018 (non presenti in questo candidate) hanno struttura simile al 2020/2023.

### Decisione

Per evitare complessità di schema drift (la colonna non è in coda ma in mezzo, causando shift di tutte le colonne successive), il candidate processa solo gli anni con "Oneri Finanziari" presente: **2019, 2021, 2022, 2024**.

I raw per gli altri anni (2012-2018, 2020, 2023) sono disponibili su BDAP ma non processati in questo candidate. Possono essere aggiunti in futuro normalizzando lo schema (aggiungendo "Oneri Finanziari" = 0 per gli anni mancanti).

## Url mapping

Tutti i dump URL seguono il pattern:
`https://bdap-opendata.rgs.mef.gov.it/SpodCkanApi/api/3/datastore/dump/{uuid}.csv`

UUID per anno:
- 2019: `a0904cd1-4cd5-40cd-9cdb-9fc404bde499`
- 2021: `f1cb1b41-d0bb-4d37-b2cb-b077a5720454`
- 2022: `7572d620-36fd-4614-90d1-8412d48f5feb`
- 2024: `d598ebd9-949d-4214-bb33-cd9c1be08f15`
