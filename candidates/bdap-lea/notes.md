# BDAP LEA — Note

## Serie storica

Candidate esteso da singolo anno (2024) a serie storica 2019-2024 (6 anni).

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

Non c'è un pattern lineare: la colonna appare e scompare senza logica apparente tra gli anni.

### Gestione

Usato `align_by_header: true` (PR toolkit #329) che allinea le righe CSV per nome colonna invece che per posizione:
- Se "Oneri Finanziari" manca → stringa vuota nella posizione attesa → `try_cast` → NULL
- Se presente → lettura normale
- Colonne extra ignorate

Anni 2012-2018 non processati (hanno struttura 22 colonne senza Oneri, compatibili ma non inclusi per focus su periodo recente).

## Url mapping

Pattern: `https://bdap-opendata.rgs.mef.gov.it/SpodCkanApi/api/3/datastore/dump/{uuid}.csv`

| Anno | UUID |
|:----:|------|
| 2019 | `a0904cd1-4cd5-40cd-9cdb-9fc404bde499` |
| 2020 | `d4816c3b-3c63-412e-aa82-ec65acaf64e7` |
| 2021 | `f1cb1b41-d0bb-4d37-b2cb-b077a5720454` |
| 2022 | `7572d620-36fd-4614-90d1-8412d48f5feb` |
| 2023 | `ac535673-49fb-4449-960e-fac8e3d14fa7` |
| 2024 | `d598ebd9-949d-4214-bb33-cd9c1be08f15` |

## Dati chiave

Spesa prevenzione sotto 5% LEA in tutti gli anni. La % più alta è 3,3% (2021).
