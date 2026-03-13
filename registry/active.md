# Filoni attivi

Usare questa nota per tenere il quadro minimo dei filoni attivi in `dataset-incubator`.

## Schema

| slug | type | stato | domanda | dataset | output minimo | target di uscita | prossimo passo |
|---|---|---|---|---|---|---|---|
| support_datasets/popolazione-istat-comunale-2019-2025 | support | intake | costruire una base comunale di popolazione residente riusabile come join | POSAS ISTAT 2019-2025 | tabella comunale per anno + base per join e controlli pro capite | support dataset interno, eventuale issue in `dataciviclab` | rilanciare la finestra multi-anno e consolidare il primo join di prova |
| project_candidates/terna-electricity-by-source | candidate | intake | come cambia il mix di generazione elettrica per fonte tra 2023 e 2024 | Terna `ElectricityBySource` 2023-2024 | raw 2023/2024 + prima lettura workbook | decidere se entra come filone ambiente in `dataciviclab/preanalysis` | verificare il run raw e fissare il primo taglio clean |
| project_candidates/dipendenti-pubblici-2021-2023 | candidate | active | il pubblico impiego sta tornando a crescere davvero, e in quali comparti? | export CSV pubblico BDAP/RGS 2021-2023 per ente e comparto | mart per anno/comparto con stock, assunti, cessati, saldo e quota donne + notebook `v0` | decidere se entra come filone lavoro pubblico / PA in `dataciviclab/preanalysis` | verificare se il primo taglio pubblico resta per comparto oppure va esteso a genere / tipo istituzione |
| project_candidates/opencoesione-pagamenti-ue-2014-2020 | candidate | intake | per regione e per tema, quanta parte dei fondi UE 2014-2020 e stata effettivamente pagata? | OpenCoesione `progetti con tracciato esteso` | tabella `regione x tema` con `finanz_ue`, `tot_pagamenti`, `ratio_spesa` | decidere se entra come filone territoriale/finanza pubblica in `dataciviclab/preanalysis` | verificare raw e clean sul CSV reale, poi lanciare il primo mart |

## Regola

Massimo 2-3 filoni vivi davvero.
