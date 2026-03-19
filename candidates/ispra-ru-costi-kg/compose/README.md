# Compose

Questa cartella contiene il layer `compose/` del filone.

Obiettivo:

- leggere gli output dei tre `source dataset`
- costruire un mart minimo `territorio x anno`
- verificare se il cross ISPRA RU regge come filone vero
- preparare un secondo mart `v2` con logica costo-performance sul `2024`

Campi minimi attesi nel mart finale:

- `territorio`
- `anno`
- `kg_per_abitante`
- `costo_per_abitante`
- `% raccolta differenziata` se disponibile e compatibile

Campi aggiuntivi previsti nel `mart_compose_v2`:

- `regione_macro`
- `cluster_demografico`
- `soglia_rd_2024`
- `soglia_costo_euro_ab_2024`
- `rd_alta_2024`
- `costo_alto_2024`
- `quadrante_costo`

Scelta adottata:

- il file SQL del cross vive anche in `compose/sql/` come riferimento architetturale
- il file SQL del `v2` vive in `compose/sql/` con la stessa logica
- il `compose/` resta documentato in una cartella propria
- l'esecuzione resta agganciata a `sources/a_ru_base/dataset.yml`, per un vincolo del toolkit sul layer `mart`
- in `sources/a_ru_base/sql/` resta quindi una copia eseguibile degli SQL del compose

Dipendenza operativa del `v2`:

- `mart_compose_v2` usa come lookup fisso il file `out/data/mart/ispra_ru_base/2024/mart_cross_comuni.parquet`
- quindi, su un clone fresco, conviene eseguire prima il `run mart` per il `2024` e solo dopo gli altri anni
- il `2024` serve per:
  - calcolare le mediane del `quadrante_costo`
  - derivare il `cluster_demografico` dalla popolazione del cross mart

Esecuzione:

```powershell
py -m toolkit.cli.app run mart --config candidates/ispra-ru-costi-kg/sources/a_ru_base/dataset.yml
```

Su clone fresco, sequenza consigliata:

```powershell
py -m toolkit.cli.app run mart --config candidates/ispra-ru-costi-kg/sources/a_ru_base/dataset.yml --years 2024
py -m toolkit.cli.app run mart --config candidates/ispra-ru-costi-kg/sources/a_ru_base/dataset.yml --years 2020,2023
```
