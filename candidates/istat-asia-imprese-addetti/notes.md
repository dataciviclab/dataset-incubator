# Note tecniche — istat-asia-imprese-addetti

## Canale

- `type: dbnomics` · provider `ISTAT` · toolkit plugin dbnomics (PR toolkit #499)
- Filtro totale: `LEGAL_FORM=TOT`, `Y_ENTER_WITH_EMPLOYEES=9`, `Y_CRAFTMEN=9`, `PERS_EMPL_SIZE_CLASS=TOTAL`

## Label territoriali

CASE NUTS1 italiano nel clean (ETAT GEO). Fallback `else` → codice.

## Relazione con istat-asia-ul

`istat-asia-ul` (#871) copre lo stesso tema al **grano comune × ATECO** (script parallelo, mirror fermo al 2020). Questo candidate copre IT + NUTS1 con serie fino al 2024 — più fresco e leggero.

## Promossa da

`esperimenti-locali/istat/datasets/istat-asia-imprese-addetti` (Tier 1, 2026-10-12).

## Run

```bash
cd candidates/istat-asia-imprese-addetti
python -m toolkit.cli.app run raw   -c dataset.yml -y 2024 --root ../../out
python -m toolkit.cli.app run clean -c dataset.yml -y 2024 --root ../../out
python -m toolkit.cli.app run mart  -c dataset.yml -y 2024 --root ../../out
```
