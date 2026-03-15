# Compose

Questa cartella contiene il layer `compose/` del filone.

Obiettivo:

- leggere gli output dei tre `source dataset`
- costruire un mart minimo `territorio x anno`
- verificare se il cross ISPRA RU regge come filone vero

Campi minimi attesi nel mart finale:

- `territorio`
- `anno`
- `kg_per_abitante`
- `costo_per_abitante`
- `% raccolta differenziata` se disponibile e compatibile

Scelta adottata:

- il file SQL del cross vive anche in `compose/sql/` come riferimento architetturale
- il `compose/` resta documentato in una cartella propria
- l'esecuzione resta agganciata a `sources/a_ru_base/dataset.yml`, per un vincolo del toolkit sul layer `mart`
- in `sources/a_ru_base/sql/` resta quindi una copia eseguibile dello stesso SQL

Esecuzione:

```powershell
py -m toolkit.cli.app run mart --config candidates/ispra-ru-costi-kg/sources/a_ru_base/dataset.yml
```
