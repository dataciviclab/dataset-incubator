# Note tecniche — istat-sbs-imprese

## Canale

- `type: dbnomics` · provider `ISTAT` · toolkit plugin dbnomics (PR toolkit #499)
- Due source: nazionale (`161_267`) + regionale (`161_268`) con `inject_column: grain`
- `clean.read.mode: all` per unire i due CSV raw

## Unità di misura

Valori monetari in **migliaia di euro** (fonte SBS). Il clean mappa:
`12110/12150/12120/13310 → mila_eur`, `11210 → conte`.

## Label territoriali

CASE NUTS1 italiano nel clean (ETAT GEO). Fallback `else` → codice.

## Promossa da

`esperimenti-locali/istat/datasets/istat-sbs-imprese` (Tier 1, 2026-10-12).

## Run

```bash
cd candidates/istat-sbs-imprese
python -m toolkit.cli.app run raw   -c dataset.yml -y 2023 --root ../../out
python -m toolkit.cli.app run clean -c dataset.yml -y 2023 --root ../../out
python -m toolkit.cli.app run mart  -c dataset.yml -y 2023 --root ../../out
```
