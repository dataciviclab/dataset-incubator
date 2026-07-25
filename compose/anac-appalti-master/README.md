# ANAC Appalti Master (compose)

**Dataset**: `anac_appalti_master`
**Tipo**: compose — unisce 8 dataset ANAC in un'unica vista

## Cos'è

Vista completa del ciclo di vita degli appalti pubblici italiani: da bando a collaudo, passando per aggiudicazione, vincitore, partecipazione, subappalti, SAL e CUP.

**Grana**: 1 riga per CIG (6.1M righe, 10 anni 2016-2025).

## Copertura

| Metrica | Valore |
|---|---|
| Righe | 6.125.177 |
| CIG distinti | 6.080.637 |
| Con vincitore | 3.986.096 (65%) |
| Con collaudo | 450.581 |
| Con CUP | 1.397.284 |

## Schema (35 colonne)

| Gruppo | Colonne |
|---|---|
| Bando | `cig`, `anno`, `oggetto_gara`, `importo_complessivo_gara`, `flag_pnrr`, `cod_cpv` |
| SA | `amministrazione`, `provincia`, `sezione_regionale` |
| Aggiudicazione | `importo_agg`, `data_agg`, `ribasso`, `offerte_ammesse`, `flag_subappalto` |
| Vincitore | `operatore`, `cf`, `tipo_soggetto`, `n_operatori` |
| Partecipazione | `n_partecipanti`, `n_imprese_partecipanti` |
| Subappalto | `n_subappalti`, `n_subappaltatori` |
| Collaudo | `esito_collaudo`, `data_collaudo`, `riserve_avanzate` |
| SAL | `n_sal`, `importo_totale_sal`, `scostamento_medio` |
| CUP | `cup` |

## Mart analitici

| Mart | Cosa |
|---|---|
| `mart_trend_annuale` | Bandi/importi/PNRR/collaudi per anno e settore |
| `mart_top_sa` | Top 100 SA per importo bandito |

## Join model

```
bandi (2016-2025) — 1 riga per CIG
 ├──cig──→ aggiudicazioni  (1:1)
 │           └──id_aggiudicazione──→ aggiudicatari (agg a 1 per CIG)
 ├──cig──→ partecipanti (agg)
 ├──cig──→ subappalti (agg)
 ├──cig──→ collaudo (agg a 1 per CIG)
 ├──cig──→ SAL (agg)
 └──cig──→ CUP (agg a 1 per CIG)
```
