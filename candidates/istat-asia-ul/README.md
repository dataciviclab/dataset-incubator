# istat_asia_ul

Candidate DI — ASIA unità locali + addetti per comune × sezione ATECO.

| | |
|---|---|
| Fonte | ISTAT SDMX `IT1/183_1163` (DICA_ASIAULP_TERRIFDATA) |
| Copertura | 2018–2024 · ~7.900 comuni × ATECO sezione |
| Metriche | `LU` unità locali · `LUEMPDAA` addetti media annua |
| Mart | `mart_asia_ul_comuni` (LU + addetti + denominazione/regione/provincia) |
| Run | clean 1.558.872 · mart 779.441 (2026-11-11) |

## Fonte e canale

Il grano **comune × ATECO** non è più aggiornato sul mirror DBnomics (fermo al 2020).
La fonte ISTAT espone ora la serie fino al **2024**: il candidate legge l'SDMX live
(`esploradati`) tramite `preprocess.py`, che spezza il fetch in 36 richieste
(2 metriche × 18 sezioni ATECO) rate-limited a ~5 req/min.

Serie aggregate IT/NUTS1 restano disponibili anche via `183_277` (vedi
`istat-asia-imprese-addetti`), ma non scendono al comune.

## Run

```bash
export TOOLKIT_ALLOW_SCRIPT_SOURCE=1
cd candidates/istat-asia-ul
python -m toolkit.cli.app run raw   -c dataset.yml -y 2024
python -m toolkit.cli.app run clean -c dataset.yml -y 2024
python -m toolkit.cli.app run mart  -c dataset.yml -y 2024
```

Il fetch completo richiede ~15 min (36 richieste rate-limited). `preprocess.py`
accetta l'anno come argomento ma scarica sempre l'intera serie (2018–2024).

Note tecniche e cautele: `notes.md`.
