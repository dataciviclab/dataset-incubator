# Notes — istat-occupazione-provinciale

## Stato

Candidate — tasso occupazione (`EMP_R`) province NUTS3 dal 2018 (run 2026-10-11 via dbnomics: **15.118** righe, 105 province).  
`UNEM_R` non restituito dal mirror con gli stessi filtri — per disoccupazione verificare SDMX o dimensioni extra.

## Fonte

**Canale 2026-10-11**: toolkit `type: dbnomics` · `ISTAT/150_915`  
Mirror: 2018–2025 su probe (allineato copertura dichiarata).  
SDMX live: solo se mirror indietro (flow **`150_915`**, non la variante `_DF_DCCV_TAXOCCU1_4` rotta con `?format=csv`).

## Filtri clean

- `FREQ=A`, province (`LENGTH(REF_AREA)=5`)
- `CITIZENSHIP=TOTAL`, `EDU_LEV_HIGHEST=99`
- Classi età: Y15-64, Y15-24, Y25-34, Y35-44, Y45-54, Y55-64
- `DATA_TYPE` in EMP_R, UNEM_R

## Run

```bash
cd candidates/istat-occupazione-provinciale
python -m toolkit.cli.app run raw   -c dataset.yml -y 2025 --root ../../out
python -m toolkit.cli.app run clean -c dataset.yml -y 2025 --root ../../out
python -m toolkit.cli.app run mart  -c dataset.yml -y 2025 --root ../../out
```
