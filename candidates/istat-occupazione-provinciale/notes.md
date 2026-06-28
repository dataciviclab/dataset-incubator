# Notes — istat-occupazione-provinciale

## Stato

Candidate v0 — solo tasso di occupazione (EMP_R) dal dataflow 150_915.
Dati provinciali (NUTS3) disponibili dal 2018 (non dal 2004, che copre solo territorio nazionale/regionale).

## Fonte

**Endpoint**: `https://esploradati.istat.it/SDMXWS/rest`
**Dataflow**: `IT1,150_915,1.0` (DCCV_TAXOCCU1 — Tasso di occupazione)
**Formato**: SDMX-CSV → letto dal reader SDMX nativo del toolkit

## Filtri applicati in clean.sql

- Solo `FREQ = 'A'` (annuale)
- Solo province NUTS3 (`LENGTH(REF_AREA) = 5`, esclusi raggruppamenti)
- Solo `CITIZENSHIP = 'TOTAL'`
- Solo `EDU_LEV_HIGHEST = '99'` (totale)
- Solo classi età: Y15-64, Y15-24, Y25-34, Y35-44, Y45-54, Y55-64
- Solo `DATA_TYPE = 'EMP_R'` (tasso occupazione)

## Dimensioni disponibili (per espansione futura)

- EDU_LEV_HIGHEST: 11 (laurea), 13 (nessun titolo), 7 (diploma), 99 (totale)
- CITIZENSHIP: ITL (italiani), FRG (stranieri), TOTAL (totale)
- AGE: tutte le classi (dal dataflow)
- SEX: 1 (maschi), 2 (femmine), 9 (totale)

## Run

```
python -m toolkit.cli.app run full \\
  --config candidates/istat-occupazione-provinciale/dataset.yml
```

Risultato: raw ✅ (53842 righe), clean ✅ (14542 righe), mart ✅

## Esempi

Top 5 province per tasso occupazione 15-64 anni (2024):
1. Firenze 74.1%
2. Prato 73.3%
3. Padova 73.1%
4. Piacenza 72.2%
5. Trieste 72.1%

Milano: 71.7% (decima)
