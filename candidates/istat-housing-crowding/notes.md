# Note tecniche - istat-housing-crowding

## Canale (2026-10-11)

- toolkit `type: dbnomics` · `ISTAT/33_179`
- SDMX live solo se mirror indietro (forzare sempre `esploradati`, non `sdmx.istat.it`)

## Perimetro v0

- `REF_AREA=IT`, `TENURE_STATUS=1+2`, altre dimensioni su totale
- `ABITAZ_AFFOLL_MED` = componenti per 100 mq (non EU-SILC crowding rate)

## Run

```bash
cd candidates/istat-housing-crowding
python -m toolkit.cli.app run raw   -c dataset.yml -y 2024 --root ../../out
python -m toolkit.cli.app run clean -c dataset.yml -y 2024 --root ../../out
python -m toolkit.cli.app run mart  -c dataset.yml -y 2024 --root ../../out
```
