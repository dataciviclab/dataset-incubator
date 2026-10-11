# Note candidate - ISTAT IPAB aree

## Canale (2026-10-11)

- toolkit `type: dbnomics` · `ISTAT/143_497`
- SDMX live: solo se mirror indietro; evitare `/all`

## Parametri

- `DATA_TYPE=59`, `MEASURE=4`, `PURCHASES_DWELLINGS=NEW_DW|EXST_DW`, `FREQ=Q`
- Livelli: Italia + macro-aree + città (aggregate, non NUTS2)
- Indice = variazione relativa base, non prezzo assoluto

## Run

```bash
cd candidates/istat-ipab-aree
python -m toolkit.cli.app run raw   -c dataset.yml -y 2024 --root ../../out
python -m toolkit.cli.app run clean -c dataset.yml -y 2024 --root ../../out
python -m toolkit.cli.app run mart  -c dataset.yml -y 2024 --root ../../out
```

## Label territoriali (2026-10-11)

CASE NUTS statico nel clean (ETAT GEO, nomi IT) + aggregati ISTAT
(`ITCD`/`ITDA`/`ITFG`/`ITCDE`). Fallback `else` → codice.
