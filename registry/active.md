# Filoni attivi

Usare questa nota per tenere il quadro minimo dei filoni attivi in `dataset-incubator`.

## Schema

| slug | type | stato | domanda | dataset | output minimo | target di uscita | prossimo passo |
|---|---|---|---|---|---|---|---|
| project_candidates/civile-flussi | candidate | active | andamento del carico della giustizia civile nei territori | Civile flussi 2014-2024 | trend per anno + confronto territoriale | `dataciviclab/preanalysis` | stringere il primo taglio analitico e fissare l'unita di confronto |
| support_datasets/popolazione-istat-comunale-2019-2025 | support | intake | costruire una base comunale di popolazione residente riusabile come join | POSAS ISTAT 2019-2025 | tabella comunale per anno + base per join e controlli pro capite | support dataset interno, eventuale issue in `dataciviclab` | rilanciare la finestra multi-anno e consolidare il primo join di prova |
| project_candidates/malasanita-struttura-mortalita | candidate | active | Le regioni con meno personale sanitario hanno tassi di mortalita evitabile piu alti? | Strutture ASL + Reparti + Ricovero per ASL (Ministero Salute) + Mortalita causa (ISTAT) — anno pivot 2022 | confronto regionale personale/mortalita evitabile 2022 | `dataciviclab/preanalysis` | completare clean/mart dopo test tecnico D riuscito (`http_file` + `unzip_first`) |
| project_candidates/terna-electricity-by-source | candidate | intake | come cambia il mix di generazione elettrica per fonte tra 2023 e 2024 | Terna `ElectricityBySource` 2023-2024 | raw 2023/2024 + prima lettura workbook | decidere se entra come filone ambiente in `dataciviclab/preanalysis` | verificare il run raw e fissare il primo taglio clean |

## Regola

Massimo 2-3 filoni vivi davvero.
