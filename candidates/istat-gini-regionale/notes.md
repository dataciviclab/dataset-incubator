# Note - istat-gini-regionale

## Source-check

- Completato il 2026-03-31, esito `go candidate`
- **Canale aggiornato 2026-10-11**: `type: dbnomics` (mirror ISTAT, no rate-limit SDMX)

## Canale

| | |
|---|---|
| DBnomics | `ISTAT/32_221` |
| Toolkit | `type: dbnomics` + dimensions `DISUG_REDDNET_GINI` × IMPUTED_RENTS 1/2 |
| Anni mirror | 2003–2024 |
| Grano | IT + NUTS2 (4 cifre) |
| SDMX live | solo se mirror indietro; id flow **`32_221`** (non `32_221_DF_DCCV_GINIREDD_1`) |

## Rischi tecnici

- **Confusione dataflow**: `DISUG_CONSUMI_GINI` (consumi) vs `DISUG_REDDNET_GINI` (reddito). Usare solo il secondo.
- SDMX live: timeout/ban da IP Lab → non usarlo come canale di run.

## Decisioni

- Entrambe le serie `IMPUTED_RENTS` (1=con fitti imputati, 2=senza) vanno tenute nel mart e documentate.
- Granularità regionale (NUTS2), non provinciale.
