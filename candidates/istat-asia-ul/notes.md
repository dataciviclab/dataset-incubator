# Note tecniche — istat-asia-ul

## Source of truth

**Candidate DI `dataset-incubator`** — copia `esperimenti-locali/lavoro-int/` **deprecated**.

| | |
|---|---|
| Canale | **`type: script`** + `preprocess.py` parallelo per ATECO |
| CI | `TOOLKIT_ALLOW_SCRIPT_SOURCE=1` già nel post-merge workflow |
| Dataset | `ISTAT/183_1163_DF_DICA_ASIAULP_TERRIFDATA_3` via DBnomics |
| Grano | comuni ISTAT 6 cifre × sezione ATECO (0010+B–S) |
| Metriche | `LU` unità locali · `LUEMPDAA` addetti media annua |
| Anni mirror | 2018–2020 |

## Perché non `local_file`

`raw_input.csv` è **gitignore** → CI non lo ha a checkout → raw mancante.

## Perché non `type: dbnomics` (plugin seriale)

~280k serie (7.9k comuni × ~18 ATECO × 2 tipi). Il plugin è sequenziale: timeout CI.  
Il preprocess parallelizza per sezione ATECO (6 worker) → ~minuti.

## Perché non SDMX live

ISTAT: 5 req/min, ban 1–2gg. DBnomics = mirror senza rate limit.

## Freschezza

Mirror comune×ATECO max **2020** (`TERRIFDATA_3`).  
IT/NUTS1 fino 2023–24: experiment `istat-asia-imprese-addetti` (`183_277`).

## Run

```bash
export TOOLKIT_ALLOW_SCRIPT_SOURCE=1
cd candidates/istat-asia-ul
python -m toolkit.cli.app run raw   -c dataset.yml -y 2020 --root ../../out
python -m toolkit.cli.app run clean -c dataset.yml -y 2020 --root ../../out
python -m toolkit.cli.app run mart  -c dataset.yml -y 2020 --root ../../out
```
