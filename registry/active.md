# Filoni attivi

Usare questa nota per tenere il quadro minimo dei filoni attivi in `dataset-incubator`.

## Schema

| slug | type | stato | domanda | dataset | output minimo | target di uscita | prossimo passo |
|---|---|---|---|---|---|---|---|
| support_datasets/popolazione-istat-comunale-2019-2025 | support | intake | costruire una base comunale di popolazione residente riusabile come join | POSAS ISTAT 2019-2025 | tabella comunale per anno + base per join e controlli pro capite | support dataset interno, eventuale issue in `dataciviclab` | rilanciare la finestra multi-anno e consolidare il primo join di prova |
| project_candidates/malasanita-struttura-mortalita | candidate | active | Le regioni con meno personale sanitario hanno tassi di mortalita evitabile piu alti? | Strutture ASL + Reparti + Ricovero per ASL (Ministero Salute) + Mortalita causa (ISTAT) - anno pivot 2022 | confronto regionale personale/mortalita evitabile 2022 | `dataciviclab/preanalysis` | consolidare notebook e primo output pubblico sul proxy regionale |

## Regola

Massimo 2-3 filoni vivi davvero.
