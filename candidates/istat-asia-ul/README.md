# istat_asia_ul

Candidate DI — ASIA unità locali + addetti per comune × sezione ATECO.

| | |
|---|---|
| Fonte | DBnomics `ISTAT/183_1163_DF_DICA_ASIAULP_TERRIFDATA_3` |
| Copertura | 2018–2020 · 7.980 comuni × ATECO sezione |
| Metriche | `LU` unità locali · `LUEMPDAA` addetti media annua |
| Mart | `mart_asia_ul_comuni` (LU + addetti + denominazione/regione/provincia) |
| Run | clean 662.890 · mart 331.445 (2026-10-11) |

## Nota freschezza

Sul mirror DBnomics il grano **comune × ATECO** si ferma al **2020** (`TERRIFDATA_3`).  
Serie più recenti: IT/NUTS1 fino a 2023–2024 (`TERRIFDATA_1` / `183_277`) — vedi `istat-asia-imprese-addetti` experiment.

## Run

```bash
export TOOLKIT_ALLOW_SCRIPT_SOURCE=1   # solo se raw type: script
# default attuale: local_file su raw_input.csv in candidates/
cd candidates/istat-asia-ul
python -m toolkit.cli.app run raw   -c dataset.yml -y 2020 --root ../../out
python -m toolkit.cli.app run clean -c dataset.yml -y 2020 --root ../../out
python -m toolkit.cli.app run mart  -c dataset.yml -y 2020 --root ../../out
```

Refresh DBnomics: `python preprocess.py 2020 raw_input.csv` e ripristinare `type: script` in `dataset.yml`.

Note tecniche: `notes.md`.
