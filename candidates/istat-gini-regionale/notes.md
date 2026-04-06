# Note — istat-gini-regionale

## Source-check

- Completato il 2026-03-31, esito `go candidate`
- Refresh 2026-04-06: endpoint SDMX stabile

## Rischi tecnici

- **API fragility**: possibili timeout su query `/all`. Lo slicing per `TIPO_DATO` e `PRES_AFF_IMP` e' sufficiente per questo dataflow (solo 2 combinazioni).
- **ID sbagliato**: `32_221_DF_DCCV_GINIREDD_1` restituisce 404. L'ID corretto e' `32_221`.
- **Confusione dataflow**: `DISUG_CONSUMI_GINI` (consumi) vs `DISUG_REDDNET_GINI` (reddito). Usare solo il secondo.

## Decisioni

- Entrambe le serie `PRES_AFF_IMP` (1=con fitti imputati, 2=senza) vanno tenute nel mart e documentate.
- Granularita regionale (NUTS2), non provinciale. Il dataflow non scende sotto il livello regionale.
