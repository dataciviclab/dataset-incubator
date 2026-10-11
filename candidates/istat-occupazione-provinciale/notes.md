# Notes — istat-occupazione-provinciale

## Stato

Candidate — tasso occupazione (`EMP_R`) province NUTS3 dal 2018.
Canale remigrato a SDMX diretto (post-fix toolkit key #444, audit #873).

## Fonte

**Canale 2026-10-11**: toolkit `type: sdmx` · `IT1/150_915` v1.0 (esploradati).
`UNEM_R` è una voce fantasma: non esiste in 150_915 né sul mirror né su SDMX
(probe live: solo `employment rate`) — rimossi dalla config e dal clean.
Per il tasso di disoccupazione servirebbe un altro dataflow ISTAT.

## Filtri clean

- `FREQ=A`, province (`LENGTH(REF_AREA)=5`)
- `CITIZENSHIP=TOTAL`, `EDU_LEV_HIGHEST=99`
- Classi età: Y15-64, Y15-24, Y25-34, Y35-44, Y45-54, Y55-64
- `DATA_TYPE = EMP_R`

## Run

```bash
cd candidates/istat-occupazione-provinciale
python -m toolkit.cli.app run raw   -c dataset.yml -y 2025 --root ../../out
python -m toolkit.cli.app run clean -c dataset.yml -y 2025 --root ../../out
python -m toolkit.cli.app run mart  -c dataset.yml -y 2025 --root ../../out
```

## Label territoriali (2026-10-11)

`territorio` / `territorio_nome` usano un **CASE NUTS statico** nel clean
(codelist ESTAT GEO, nomi italiani). NUTS stabili — aggiornamento solo se
cambiano confini. Codici ISTAT IT1xx (province post-2004, non in GEO 2021) (`IT108`–`IT111`)
mappati: IT108=Monza e della Brianza, IT109=Fermo, IT110=Barletta-Andria-Trani, IT111=Sud Sardegna. Aggregati ISTAT (`ITCD`, `ITDA`,
`ITFG`, `ITCDE`) mappati a label descrittive.

`eta`: label leggibili da codici AGE SDMX (`Y15-24` → `15-24 anni`).
