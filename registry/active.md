# Filoni attivi

Usare questa nota per tenere il quadro minimo dei filoni attivi in `dataset-incubator`.

## Schema

| slug | type | stato | domanda | dataset | output minimo | target di uscita | prossimo passo |
|---|---|---|---|---|---|---|---|
| support_datasets/popolazione-istat-comunale-2019-2025 | support | intake | costruire una base comunale di popolazione residente riusabile come join | POSAS ISTAT 2019-2025 | tabella comunale per anno + base per join e controlli pro capite | support dataset interno, eventuale issue in `dataciviclab` | rilanciare la finestra multi-anno e consolidare il primo join di prova |
| project_candidates/dipendenti-pubblici-2021-2023 | candidate | active | il pubblico impiego sta tornando a crescere davvero, e in quali comparti? | export CSV pubblico BDAP/RGS 2021-2023 per ente e comparto | mart per anno/comparto con stock, assunti, cessati, saldo e quota donne + notebook `v0` | decidere se entra come filone lavoro pubblico / PA in `dataciviclab/preanalysis` | verificare se il primo taglio pubblico resta per comparto oppure va esteso a genere / tipo istituzione |
| project_candidates/opencoesione-pagamenti-ue-2014-2020 | candidate | intake | per regione e per tema, quanta parte dei fondi UE 2014-2020 e stata effettivamente pagata? | OpenCoesione `progetti con tracciato esteso` | tabella `regione x tema` con `finanz_ue`, `tot_pagamenti`, `ratio_spesa` | decidere se entra come filone territoriale/finanza pubblica in `dataciviclab/preanalysis` | verificare raw e clean sul CSV reale, poi lanciare il primo mart |
| project_candidates/ispra-consumo-suolo | candidate | intake | quali territori continuano a consumare più suolo e quanto pesa il consumo recente rispetto allo stock accumulato? | ISPRA consumo di suolo comunale 2006-2024 | clean minimo + mart comunale + decisione su perimetro | decidere se entra come filone ambiente in `dataciviclab/preanalysis` | verificare lettura XLSX nel toolkit e formalizzare il candidate |
| project_candidates/ispra-ru-costi-kg | candidate | active | chi spende di più nella gestione dei rifiuti differenzia meglio, o l'efficienza non segue la spesa? | ISPRA catasto rifiuti: RU base + kg/ab + costo/ab, 2020-2024 | mart_compose su perimetro pulito + notebook `v1` con domande civiche + grafici esportabili | preanalysis pubblica su `dataciviclab` + valutazione v2 dashboard pilota | rileggere notebook `v0`, decidere perimetro temporale definitivo, aprire issue pubblica |
| project_candidates/aifa-spesa-consumo-2016-2024 | candidate | intake - run 2022-2024 OK | come cambia tra regioni e nel tempo la spesa farmaceutica convenzionata per classi terapeutiche? | AIFA spesa e consumo farmaceutica convenzionata 2016-2024 (filone completo); run verificato su 2022-2024 | clean + mart mensile regione x ATC4 su 2022-2024; estendere a 2016-2021 | decidere se entra come filone sanità in `dataciviclab/preanalysis` | scaricare anni 2016-2021, aprire discussion in dataciviclab con primi numeri |

## Regola

Massimo 2-3 filoni vivi davvero.
