# Note tecniche — istat-sbs-imprese

## Canale

- `type: dbnomics` · provider `ISTAT` · toolkit plugin dbnomics (PR toolkit #499)
- Due source: nazionale (`161_267`) + regionale (`161_268`) con `inject_column: grain`
- `clean.read.mode: all` per unire i due CSV raw

## Unità di misura

Valori monetari in **migliaia di euro** (fonte SBS). Il clean mappa:
`12110/12120/12150/12170/13310/13320/13330/15110 → mila_eur`,
`16150 → migliaia_ore`, `11110/11210 → conte`.

## Label territoriali

CASE NUTS1 italiano nel clean (ETAT GEO). Fallback `else` → codice.

## Promossa da

`esperimenti-locali/istat/datasets/istat-sbs-imprese` (Tier 1, 2026-10-12).

## Run

```bash
cd candidates/istat-sbs-imprese
python -m toolkit.cli.app run raw   -c dataset.yml -y 2024 --root ../../out
python -m toolkit.cli.app run clean -c dataset.yml -y 2024 --root ../../out
python -m toolkit.cli.app run mart  -c dataset.yml -y 2024 --root ../../out
```

## Estensione 2026-10 — ore, costo del lavoro, GOS, investimenti

Verifica DBnomics sul dataflow nazionale `161_267_DF_DCSP_SBSNAZ_1`: 118
`DATA_TYPE` disponibili, 17 anni (2008–2024) per NACE C. Aggiunti al perimetro:

- `12170` risultato lordo di gestione (GOS)
- `13310` costi del personale, `13320` salari e stipendi, `13330` contributi sociali
- `15110` investimenti fissi lordi
- `16150` ore lavorate dai dipendenti (migliaia di ore)
- `11110` imprese

Il regionale resta **lean** (`12110`, `12150`, `13310`, `13320`, `11210`):
su `ITC4/C` le serie `12170`, `13330`, `16150`, `11110` risultano vuote e
`15110` si ferma al 2015. La matrice settoriale completa va quindi costruita
sul livello nazionale.

Follow-up possibile dallo stesso dataflow: quartili `E12150_PER_ADD_*`,
`E13310_PER_DIP_*`, `N00001_*` (wage-adjusted labour productivity) e classi
dimensionali `PERS_EMPL_SIZE_CLASS` (micro, piccole, medie, grandi). Oggi il
perimetro resta su `TOTAL` per non moltiplicare le righe.

## Mart settoriale

`mart_sbs_settore` è una matrice nazionale `anno × NACE` (wide) costruita dal
clean. Unità: `*_mila_eur` in migliaia di euro, `ore_migliaia` in migliaia di
ore; i rapporti `*_per_ora_eur` sono euro/ora e le quote sono percentuali.

- `va_per_ora_eur` = `va_mila_eur / ore_migliaia` (migliaia € / migliaia ore = €/ora)
- `quota_lavoro_pct` = costi del personale / VA
- `gos_su_va_pct` = GOS / VA (proxy di redditività, non profitto netto)
- `investimenti_su_va_pct` = investimenti fissi lordi / VA

Il mart è validato con `primary_key [anno, nace_codice]` e range su quote,
rapporti e valori orari.

## Estensione filiere (2026-10)

- Aggiunti al dataflow nazionale `161_267_DF_DCSP_SBSNAZ_1` i NACE `10`, `11`,
  `12`, `47`.
- Il regionale resta lean e sections-only: il dettaglio 2 cifre è nazionale.
- `mart_sbs_settore` filtra `length(nace_codice) = 1` per non mescolare sezioni
  e codici a 2 cifre.
- `mart_sbs_filiere` copre industria alimentare (`10`), bevande (`11`), tabacco
  (`12`) e commercio al dettaglio (`47`).
- Agricoltura (`A`/`01`) non disponibile in SBS per `12150`: resta su RICA.
- `11210` (unità locali) non è nel nazionale; `mart_sbs_filiere` include `11110`
  (imprese) e non le unità locali.
- Unità invariate: migliaia di euro, migliaia di ore, euro/ora, percentuali.
