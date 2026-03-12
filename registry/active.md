# Filoni attivi

Usare questa nota per tenere il quadro minimo dei filoni attivi in `dataset-incubator`.

## Schema

| slug | type | stato | domanda | dataset | output minimo | target di uscita | prossimo passo |
|---|---|---|---|---|---|---|---|
| support_datasets/popolazione-istat-comunale-2019-2025 | support | intake | costruire una base comunale di popolazione residente riusabile come join | POSAS ISTAT 2019-2025 | tabella comunale per anno + base per join e controlli pro capite | support dataset interno, eventuale issue in `dataciviclab` | rilanciare la finestra multi-anno e consolidare il primo join di prova |
| project_candidates/malasanita-struttura-mortalita | candidate | active | Le regioni con meno personale sanitario hanno tassi di mortalita evitabile piu alti? | Strutture ASL + Reparti + Ricovero per ASL (Ministero Salute) + Mortalita causa (ISTAT) - anno pivot 2022 | v1 (cod_causa=25) + v2 (Euro-2013 proxy) + v3 (broad age-standardization 30+) | `dataciviclab/preanalysis` | decisione presa (issue #24): v3 e` la baseline raccomandata; prossimo passo: promozione a `dataciviclab/preanalysis` |
| project_candidates/terna-electricity-by-source | candidate | intake | come cambia il mix di generazione elettrica per fonte tra 2023 e 2024 | Terna `ElectricityBySource` 2023-2024 | raw 2023/2024 + prima lettura workbook | decidere se entra come filone ambiente in `dataciviclab/preanalysis` | verificare il run raw e fissare il primo taglio clean |

## Regola

Massimo 2-3 filoni vivi davvero.
