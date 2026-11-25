# Note tecniche — istat-asia-ul

## Source of truth

**Candidate DI `dataset-incubator`** — copia `esperimenti-locali/lavoro-int/` **deprecated**.

| | |
|---|---|
| Canale | **`type: script`** + `preprocess.py` su ISTAT SDMX live |
| CI | `TOOLKIT_ALLOW_SCRIPT_SOURCE=1` già nel post-merge workflow |
| Dataflow | `IT1 / 183_1163` (DICA_ASIAULP_TERRIFDATA) |
| Key | `A..<DATA_TYPE>.<ATECO>.TOTAL` per 18 sezioni (0010 + B–S) |
| Grano | comuni ISTAT 6 cifre × sezione ATECO |
| Metriche | `LU` unità locali · `LUEMPDAA` addetti media annua |
| Anni | 2018–2024 |

## Perché `type: script`

~1,5M osservazioni (7,9k comuni × 18 sezioni × 2 metriche × 7 anni). Il plugin
SDMX fa una richiesta unica: troppo grande e lenta (oltre 4 min per 6 sezioni).
`preprocess.py` spezza in **36 richieste piccole** (2 metriche × 18 sezioni) con:
- rate limiter condiviso a ~5 req/min (limite ISTAT);
- 4 worker in parallelo;
- scrittura incrementale (non tiene 1,5M righe in memoria);
- 4 retry con backoff.

Durata misurata: **~14 min**. Il raw timeout in `dataset.yml` è 3000s.

## Perché non DBnomics

Il mirror `183_1163_DF_DICA_ASIAULP_TERRIFDATA_3` è fermo al **2020** (ultimo
indice 2023-01). La fonte ISTAT espone 2021–2024.

## Perché non `local_file`

`raw_input.csv` è **gitignore** → CI non lo ha a checkout → raw mancante.

## Cautele

- **Comuni storici**: la join con `istat_elenco_comuni` (anagrafica 2026) lascia
  ~400 comuni/anno senza `regione`/`sigla_provincia`. Sono comuni soppressi o
  fusi dopo l'anno di riferimento (es. 001005, 001138). Il dato resta valido a
  livello comunale; manca solo l'arricchimento territoriale. Non è una
  regressione: la join era già `LEFT JOIN` prima del cambio fonte.
- **Codici `INH_*`**: la risposta SDMX include righe con `REF_AREA` tipo
  `INH_GE250001` (località abitate). `preprocess.py` le scarta prima del CSV
  (il clean faceva lo stesso filtro `length(ref_area)=6`).
- **Revisioni**: ASIA ricalcola gli anni precedenti a ogni rilascio; i valori
  2018–2023 possono differire dalla versione pubblicata in precedenza.

## Run

```bash
export TOOLKIT_ALLOW_SCRIPT_SOURCE=1
cd candidates/istat-asia-ul
python -m toolkit.cli.app run raw   -c dataset.yml -y 2024
python -m toolkit.cli.app run clean -c dataset.yml -y 2024
python -m toolkit.cli.app run mart  -c dataset.yml -y 2024
```
