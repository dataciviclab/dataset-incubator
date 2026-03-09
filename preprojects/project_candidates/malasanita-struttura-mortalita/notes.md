# Notes - malasanita-struttura-mortalita

## Stato tecnico

Nel branch `feat/malasanita-mart-hardening` il candidato ha una prima base eseguibile e verificata:

- `A` raw/clean/mart ok
- `C` raw/clean/mart ok
- `D` raw/clean/mart ok
- compose finale `A + C + D` ok

Join finale verificato:
- `join_c_ok = 21/21`
- `join_d_ok = 21/21`

## Architettura adottata

Pattern multi-fonte:

- un source dataset per ogni fonte
- un mart regionale minimo per fonte
- un compose finale che legge solo output gia aggregati

Implementazione attuale:

- `sources/a_strutture_asl/sql/mart.sql`
- `sources/c_strutture_ricovero_asl/sql/mart.sql`
- `sources/d_mortalita_istat/sql/mart.sql`
- `sources/a_strutture_asl/sql/mart_compose_regioni.sql`

Il compose finale e` agganciato al dataset di `A` per un vincolo del toolkit: il file SQL del mart deve stare sotto la base dir del dataset che lo esegue.

## Fonte D

La fonte `D` e` il punto metodologicamente piu delicato.

Problema verificato:
- sommare tutte le righe del clean sovraconta i decessi

Scelta adottata nella v1:
- `cod_sesso = 3`
- `cod_classe_eta = 9`
- `cod_titolo_studio = 9`
- `cod_causa = 25`

Questo produce una riga per territorio regionale con:
- `decessi_totali`
- `pop_media_30_plus`
- `tasso_std_10000_30_plus`
- `tasso_std_100k_30_plus`

Quindi:
- la v1 usa **mortalita totale regionale 30+**
- non usa ancora **mortalita evitabile**

## Join regionale

Fonte A e C:
- `codice_regione` a 3 cifre Ministero

Fonte D:
- `cod_territorio` ISTAT a 2 cifre

Mapping usato nel compose:
- `LEFT(codice_regione, 2)` per le regioni ordinarie
- eccezioni:
  - `041 -> 21` Bolzano
  - `042 -> 22` Trento

## Limiti della v1

- `B` non entra ancora nel compose finale
- `D` e` ancora un proxy regionale, non la metrica finale desiderata
- i tassi `30+` di `D` non vanno confusi con un denominatore generale di popolazione residente

## Prossima v2

Per una versione piu forte del progetto:

- costruire una definizione esplicita di mortalita evitabile da `D`
- valutare un `mart_regioni` utile anche per `B`
- decidere se il compose finale debba restare flat o sdoppiarsi in due tavole (`strutture` / `mortalita`)
