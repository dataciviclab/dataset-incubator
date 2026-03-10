# malasanita-struttura-mortalita

## Domanda

Le regioni con meno personale sanitario hanno livelli piu alti di mortalita evitabile?

## Dataset

Anno pivot: **2022**, unico anno di sovrapposizione completa tra le fonti del nucleo.

| ID | Fonte | Copertura | Formato |
|---|---|---|---|
| A | Strutture e attivita ASL - dati.salute.gov.it | fino al 2022 | CSV/XLSX |
| B | Reparti strutture di ricovero - dati.salute.gov.it | fino al 2022 | CSV/XLSX |
| C | Strutture ricovero per ASL - dati.salute.gov.it | fino al 2022 | CSV/XLSX |
| D | Mortalita per causa - ISTAT | fino al 2022 | ZIP -> XLSX |

Fonti di secondo livello, fuori dalla preanalysis finche il nucleo non regge:
- AGENAS/SIMES
- MedMal Marsh

## Stato attuale

Il candidato e` attivo e ha ora una prima struttura multi-fonte eseguibile:

- `A` espone un `mart_regioni` con personale territoriale e residenti
- `C` espone un `mart_regioni` con personale e dotazione ospedaliera
- `D` espone un `mart_regioni` con mortalita totale regionale sul perimetro `30+`
- `A` espone anche un `mart_compose_regioni` finale che legge i mart di `A/C/D`

Questa v1 non misura ancora la **mortalita evitabile**. Usa invece un proxy regionale basato su:
- `decessi_totali`
- `pop_media_30_plus`
- `tasso_std_10000_30_plus`
- `tasso_std_100k_30_plus`

## Output minimo atteso

- tabella regionale 2022 con indicatori di struttura sanitaria e mortalita totale regionale
- verifica che il join regionale A/C/D sia stabile su 21 unita territoriali
- nota metodologica che distingua chiaramente proxy v1 e obiettivo finale su mortalita evitabile

## Criterio di promozione

- source dataset `A/C/D` eseguibili
- join regionale stabile
- output regionale leggibile
- perimetro metodologico dichiarato in modo onesto

La promozione forte resta comunque subordinata a una v2 che costruisca davvero la metrica di mortalita evitabile.

## Run

I source dataset sono eseguibili dal repo `dataset-incubator`.

Ordine pratico:

```powershell
py -m toolkit.cli.app run all --config preprojects/project_candidates/malasanita-struttura-mortalita/sources/a_strutture_asl/dataset.yml
py -m toolkit.cli.app run all --config preprojects/project_candidates/malasanita-struttura-mortalita/sources/c_strutture_ricovero_asl/dataset.yml
py -m toolkit.cli.app run all --config preprojects/project_candidates/malasanita-struttura-mortalita/sources/d_mortalita_istat/dataset.yml
py -m toolkit.cli.app run mart --config preprojects/project_candidates/malasanita-struttura-mortalita/sources/a_strutture_asl/dataset.yml
```

L'ultimo comando rigenera anche il compose finale:

- `out/data/mart/malasanita_a_strutture_asl/2022/mart_compose_regioni.parquet`

## Nota

Il download live del Ministero puo fallire dal terminale. Nel branch di hardening i source dataset sono configurati per lavorare con file locali in `inputs/`.
