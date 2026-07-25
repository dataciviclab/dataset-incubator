# ANAC Appalti Master (compose)

**Dataset**: `anac_appalti_master`
**Tipo**: compose — unisce 8 dataset ANAC in un'unica vista

## Cos'è

Vista completa del ciclo di vita degli appalti pubblici italiani: da bando a collaudo, passando per aggiudicazione, vincitore, partecipazione, subappalti, SAL e CUP.

10.4M righe su 10 anni (2016-2025), 8 dataset ANAC unificati.

## Schema (34 colonne)

| Gruppo | Colonne |
|---|---|
| Bando | `cig`, `anno`, `oggetto_gara`, `importo_complessivo_gara`, `oggetto_principale`, `flag_pnrr`, `cod_cpv` |
| SA | `amministrazione`, `provincia`, `sezione_regionale` |
| Aggiudicazione | `importo_agg`, `data_agg`, `ribasso`, `offerte_ammesse`, `flag_subappalto`, `criterio_agg` |
| Vincitore | `operatore`, `cf`, `tipo_soggetto` |
| Partecipazione | `n_partecipanti`, `n_imprese_partecipanti` |
| Subappalto | `n_subappalti`, `n_subappaltatori` |
| Collaudo | `esito_collaudo`, `data_collaudo`, `riserve_avanzate`, `contenzioso` |
| SAL | `n_sal`, `importo_totale_sal`, `scostamento_medio` |
| CUP | `cup` |

## Mart analitici

| Mart | Cosa | Righe |
|---|---|---|
| `mart_trend_annuale` | Bandi/importi/PNRR/collaudi per anno e settore | 32 |
| `mart_top_sa` | Top 100 SA per importo bandito | 100 |

## Join model

```
bandi (2016-2025)
 ├──cig──→ aggiudicazioni
 │           └──id_aggiudicazione──→ aggiudicatari
 ├──cig──→ partecipanti (agg)
 ├──cig──→ subappalti (agg)
 ├──cig──→ collaudo
 ├──cig──→ SAL (agg)
 └──cig──→ CUP (bridge)
```
