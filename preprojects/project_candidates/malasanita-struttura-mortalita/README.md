# malasanita-struttura-mortalita

## Domanda

Le regioni con meno personale sanitario hanno livelli piu alti di mortalita evitabile?

## Dataset

Anno pivot: **2022**, unico anno di sovrapposizione completa tra le fonti del nucleo.

| ID | Fonte | Copertura | Formato |
|---|---|---|---|
| A | Strutture e attivita ASL - dati.salute.gov.it | fino al 2022 | CSV/XLSX |
| B | Reparti strutture di ricovero - dati.salute.gov.it | fino al 2022 | CSV/XLSX |
| C | Strutture ricovero per ASL - dati.salute.gov.it | fino al 2022 | CSV/XLSX |
| D | Mortalita per causa - ISTAT | fino al 2022 | ZIP -> XLSX |

Fonti di secondo livello, fuori dalla preanalysis finche il nucleo non regge:
- AGENAS/SIMES
- MedMal Marsh

## Stato attuale

Il candidato ha una struttura multi-fonte eseguibile e due notebook di preanalysis con artifact separati:

- `A` espone un `mart_regioni` con personale territoriale e residenti
- `C` espone un `mart_regioni` con personale e dotazione ospedaliera
- `D` espone due mart distinti: `mart_regioni_v1` (mortalita totale 30+) e `mart_regioni_v2` (Euro-2013 proxy)
- `A` espone due compose distinti: `mart_compose_regioni_v1` e `mart_compose_regioni_v2`

### Matrice notebook — artifact — metrica

| Notebook | Artifact parquet | Metrica mortalita | Metodologia |
|---|---|---|---|
| `malasanita_preanalysis_v1.ipynb` | `mart_compose_regioni_v1.parquet` | `decessi_30plus_per_100k_pop_totale` | baseline storica — mortalita totale 30+ (main) |
| `malasanita_preanalysis_v2.ipynb` | `mart_compose_regioni_v2.parquet` | `decessi_evitabili_30plus_per_100k_pop_totale` | Euro-2013 proxy — 12 cause amenable/preventable |

### v1 — baseline storica (main)

Proxy mortalita totale 30+ (`cod_causa=25`). Notebook: `malasanita_preanalysis_v1.ipynb`.

### v2 — branch evolutivo Euro-2013

Proxy Euro-2013 (12 cause amenable/preventable, tasso grezzo 30+).
Notebook: `malasanita_preanalysis_v2.ipynb`.

**Nota denominatore ibrido:** il campo `decessi_evitabili_30plus_per_100k_pop_totale`
nel compose finale usa numeratore 30+ e denominatore popolazione totale regionale.
Non e` un tasso grezzo canonico — documentato nel mart, nel compose e nel notebook.

**Nota dati fonte C:** Molise e Valle d'Aosta mostrano valori anomali su `personale_osp_per_100k`
(possibile problema di copertura dati, segnalato in PR #15). Interpretare con cautela.

## Output disponibile

- `out/data/mart/malasanita_a_strutture_asl/2022/mart_compose_regioni_v1.parquet` — tabella regionale 2022, metrica v1
- `out/data/mart/malasanita_a_strutture_asl/2022/mart_compose_regioni_v2.parquet` — tabella regionale 2022, metrica v2
- join A/C/D stabile su 21 unita territoriali (join_c_ok e join_d_ok = 21/21)
- due notebook eseguibili (v1 e v2) con artifact separati e narrativa metodologica esplicita

## Criterio di promozione

- [x] source dataset `A/C/D` eseguibili
- [x] join regionale stabile
- [x] output regionale leggibile
- [x] perimetro metodologico dichiarato in modo onesto
- [ ] age-standardizzazione esplicita (v3, fuori scope preanalysis)

## Run

I source dataset sono eseguibili dal repo `dataset-incubator`.

Ordine pratico:

```powershell
py -m toolkit.cli.app run all --config preprojects/project_candidates/malasanita-struttura-mortalita/sources/a_strutture_asl/dataset.yml
py -m toolkit.cli.app run all --config preprojects/project_candidates/malasanita-struttura-mortalita/sources/c_strutture_ricovero_asl/dataset.yml
py -m toolkit.cli.app run all --config preprojects/project_candidates/malasanita-struttura-mortalita/sources/d_mortalita_istat/dataset.yml
py -m toolkit.cli.app run mart --config preprojects/project_candidates/malasanita-struttura-mortalita/sources/a_strutture_asl/dataset.yml
```

L'ultimo comando rigenera i due compose finali:

- `out/data/mart/malasanita_a_strutture_asl/2022/mart_compose_regioni_v1.parquet`
- `out/data/mart/malasanita_a_strutture_asl/2022/mart_compose_regioni_v2.parquet`

