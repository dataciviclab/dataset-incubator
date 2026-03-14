# Compose

Questa cartella documenta il `compose/` finale del filone.

Obiettivo previsto:

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

- il `compose` eseguibile e` agganciato a `sources/a_ru_base/dataset.yml`
- il file SQL reale e`:
  - `sources/a_ru_base/sql/mart_cross_comuni.sql`

Motivo:

- il toolkit esegue il mart dal `dataset.yml` di un source dataset
- il `compose/` qui resta documentale, come nel pattern multi-fonte di `malasanita`
