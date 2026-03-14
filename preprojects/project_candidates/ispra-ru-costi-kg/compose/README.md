# Compose

Questa cartella ospitera il `compose/` finale del filone.

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

Il `compose/` verra formalizzato con `dataset.yml` e SQL solo dopo la verifica reale delle tre sorgenti.
