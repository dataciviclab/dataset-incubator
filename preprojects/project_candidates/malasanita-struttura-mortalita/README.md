# malasanita-struttura-mortalita

> **Promosso.** Il lavoro vivo e in `dataciviclab/preanalysis/malasanita-struttura-mortalita`. I file qui sotto sono storico di incubazione.

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

Il candidato ha una struttura multi-fonte eseguibile e tre notebook di preanalysis con artifact separati:

- `A` espone un `mart_regioni` con personale territoriale e residenti
- `C` espone un `mart_regioni` con personale e dotazione ospedaliera
- `D` espone tre mart distinti: `mart_regioni_v1` (mortalita totale 30+), `mart_regioni_v2` (Euro-2013 proxy) e `mart_regioni_v3` (broad age-standardization 30+)
- `A` espone tre compose distinti: `mart_compose_regioni_v1`, `mart_compose_regioni_v2` e `mart_compose_regioni_v3`

### Matrice notebook — artifact — metrica

| Notebook | Artifact parquet | Metrica mortalita | Metodologia |
|---|---|---|---|
| `malasanita_preanalysis_v1.ipynb` | `mart_compose_regioni_v1.parquet` | `decessi_30plus_per_100k_pop_totale` | baseline storica — mortalita totale 30+ (main) |
| `malasanita_preanalysis_v2.ipynb` | `mart_compose_regioni_v2.parquet` | `decessi_evitabili_30plus_per_100k_pop_totale` | Euro-2013 proxy — 12 cause amenable/preventable, tasso grezzo 30+ |
| `malasanita_preanalysis_v3.ipynb` | `mart_compose_regioni_v3.parquet` | `tasso_std_broad_evitabile_100k_30plus` | broad age-standardization 30+ su 3 bande età, pesi ESP2013 aggregati |

### v1 — baseline storica (main)

Proxy mortalita totale 30+ (`cod_causa=25`). Notebook: `malasanita_preanalysis_v1.ipynb`.

### v2 — proxy grezzo Euro-2013 (supporto)

Proxy Euro-2013 (12 cause amenable/preventable, tasso grezzo 30+).
Notebook: `malasanita_preanalysis_v2.ipynb`.

Ruolo attuale: proxy grezzo di supporto, documentato e mantenuto, non eliminato.
La v3 e` la metrica raccomandata per il confronto inter-regionale (vedi sotto).

**Nota denominatore ibrido:** il campo `decessi_evitabili_30plus_per_100k_pop_totale`
nel compose finale usa numeratore 30+ e denominatore popolazione totale regionale.
Non e` un tasso grezzo canonico — documentato nel mart, nel compose e nel notebook.

**Nota dati fonte C:** Molise e Valle d'Aosta mostrano valori anomali su `personale_osp_per_100k`
(possibile problema di copertura dati, segnalato in PR #15). Interpretare con cautela.

### v3 — broad age-standardization 30+ ⭐ baseline raccomandata

**Metrica raccomandata per il confronto inter-regionale** (decisione su issue #24).

Stesse 12 cause della v2, ma con standardizzazione esplicita su tre classi età disponibili in `D`:
`30-69`, `70-84`, `85+`.

La fonte ISTAT non consente una ESP2013 piena a 5 anni; per questo la v3 aggrega i pesi
ESP2013 sulle tre bande presenti nel dataset e calcola un tasso standardizzato broad.

Il campo principale nel compose v3 e` `tasso_std_broad_evitabile_100k_30plus`.
Questa scelta elimina il denominatore ibrido della v2 e produce una metrica piu difendibile
per il confronto inter-regionale, pur restando piu grossolana di una age-standardization piena.

Validazione: correlazione broad vs `tasso_std_10000` ISTAT (totale cause) ~0.99.
Il ranking regionale cambia in modo non cosmetics rispetto alla v2 (avg abs shift 3.8, max 10):
Liguria scende da #1 (artefatto demografico) a #9; Campania sale da #11 a #1.

## Output disponibile

- `out/data/mart/malasanita_a_strutture_asl/2022/mart_compose_regioni_v1.parquet` — tabella regionale 2022, metrica v1
- `out/data/mart/malasanita_a_strutture_asl/2022/mart_compose_regioni_v2.parquet` — tabella regionale 2022, metrica v2
- `out/data/mart/malasanita_a_strutture_asl/2022/mart_compose_regioni_v3.parquet` — tabella regionale 2022, metrica v3
- join A/C/D stabile su 21 unita territoriali (join_c_ok e join_d_ok = 21/21)
- tre notebook eseguibili (v1, v2, v3) con artifact separati e narrativa metodologica esplicita

## Criterio di promozione

- [x] source dataset `A/C/D` eseguibili
- [x] join regionale stabile
- [x] output regionale leggibile
- [x] perimetro metodologico dichiarato in modo onesto
- [x] age-standardizzazione esplicita broad 30+ (v3)

## Run

I source dataset sono eseguibili dal repo `dataset-incubator`.

Ordine pratico:

```powershell
py -m toolkit.cli.app run all --config preprojects/project_candidates/malasanita-struttura-mortalita/sources/a_strutture_asl/dataset.yml
py -m toolkit.cli.app run all --config preprojects/project_candidates/malasanita-struttura-mortalita/sources/c_strutture_ricovero_asl/dataset.yml
py -m toolkit.cli.app run all --config preprojects/project_candidates/malasanita-struttura-mortalita/sources/d_mortalita_istat/dataset.yml
py -m toolkit.cli.app run mart --config preprojects/project_candidates/malasanita-struttura-mortalita/sources/a_strutture_asl/dataset.yml
```

L'ultimo comando rigenera i tre compose finali:

- `out/data/mart/malasanita_a_strutture_asl/2022/mart_compose_regioni_v1.parquet`
- `out/data/mart/malasanita_a_strutture_asl/2022/mart_compose_regioni_v2.parquet`
- `out/data/mart/malasanita_a_strutture_asl/2022/mart_compose_regioni_v3.parquet`
