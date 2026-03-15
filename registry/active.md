# Filoni attivi

Usare questa nota per tenere il quadro minimo dei filoni attivi in `dataset-incubator`.

## Schema

| slug | type | stato | domanda | dataset | output minimo | target di uscita | prossimo passo |
|---|---|---|---|---|---|---|---|
| support_datasets/popolazione-istat-comunale-2019-2025 | support | intake | costruire una base comunale di popolazione residente riusabile come join | POSAS ISTAT 2019-2025 | tabella comunale per anno + base per join e controlli pro capite | support dataset interno, eventuale issue in `dataciviclab` | rilanciare la finestra multi-anno e consolidare il primo join di prova |
| project_candidates/terna-electricity-by-source | candidate | intake | come cambia il mix di generazione elettrica per fonte tra 2023 e 2024 | Terna `ElectricityBySource` 2023-2024 | raw 2023/2024 + prima lettura workbook | decidere se entra come filone ambiente in `dataciviclab/preanalysis` | verificare il run raw e fissare il primo taglio clean |
| project_candidates/opencoesione-pagamenti-ue-2014-2020 | candidate | intake | per regione e per tema, quanta parte dei fondi UE 2014-2020 e stata effettivamente pagata? | OpenCoesione `progetti con tracciato esteso` | tabella `regione x tema` con `finanz_ue`, `tot_pagamenti`, `ratio_spesa` | decidere se entra come filone territoriale/finanza pubblica in `dataciviclab/preanalysis` | verificare raw e clean sul CSV reale, poi lanciare il primo mart |
| project_candidates/ispra-ru-costi-kg | candidate | intake | i territori che producono meno rifiuti urbani o raccolgono meglio spendono anche meno per abitante? | nucleo ISPRA RU base + kg per abitante + costo per abitante | nota di compatibilita + primo join di prova + mart minimo `territorio x anno` | decidere se regge come filone ambiente o resta support dataset | recuperare le due tabelle aggiuntive e verificare chiavi e annualita comuni |
| project_candidates/aifa-spesa-consumo-2016-2024 | candidate | intake - run 2022-2024 OK | come cambia tra regioni e nel tempo la spesa farmaceutica convenzionata per classi terapeutiche? | AIFA spesa e consumo farmaceutica convenzionata 2016-2024 (filone completo); run verificato su 2022-2024 | clean + mart mensile regione x ATC4 su 2022-2024; estendere a 2016-2021 | decidere se entra come filone sanita in `dataciviclab/preanalysis` | scaricare anni 2016-2021, aprire discussion in dataciviclab con primi numeri |

## Regola

Massimo 2-3 filoni vivi davvero.
