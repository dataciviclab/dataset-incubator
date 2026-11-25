# Note tecniche — istat-va-branca

## Canale

- `type: dbnomics` · provider `ISTAT` · toolkit plugin dbnomics (PR toolkit #499)
- Eddition pin `2025M6` per stabilità della serie
- Precedentemente in `esperimenti-locali` con root sbagliata (`../out` → raw duplicato)

## Label territoriali

CASE NUTS2 italiano nel clean (ETAT GEO, nomi IT). Fallback `else` → codice.

## Filtri clean

- `DATA_TYPE_AGGR = B1G_B_W2_S1` (VA)
- `VALUATION IN (V, L_2020)` — prezzi correnti e costanti 2020
- `BRKDW_INDUSTRY_NACE_REV2 <> 'Z'` (escluso non classificato)
- ultima edizione per REF_AREA × DATA_TYPE_AGGR

## Promossa da

`esperimenti-locali/istat/datasets/istat-va-branca` (Tier 1, 2026-10-12).

## Run

```bash
cd candidates/istat-va-branca
python -m toolkit.cli.app run raw   -c dataset.yml -y 2023 --root ../../out
python -m toolkit.cli.app run clean -c dataset.yml -y 2023 --root ../../out
python -m toolkit.cli.app run mart  -c dataset.yml -y 2023 --root ../../out
```
