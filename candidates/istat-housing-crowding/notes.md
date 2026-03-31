# Note tecniche - istat-housing-crowding

## Perimetro v0 scelto

- `REF_AREA=IT`
- `TENURE_STATUS=1+2`
- tutte le altre dimensioni su totale
- serie storica completa disponibile nel flow

## Nota semantica

`ABITAZ_AFFOLL_MED` non e il tasso EU-SILC di sovraffollamento.
Qui il pilot usa un indicatore di densita abitativa media (`componenti per 100 mq`).

## Nota tecnica importante

Per il dataflow `33_179`, `https://sdmx.istat.it/SDMXWS/rest/dataflow/IT1/33_179`
restituisce `500` nel setup attuale, mentre `https://esploradati.istat.it/SDMXWS/rest`
risponde correttamente sia per metadata sia per data.

Per questo il candidate forza:

- `client.metadata_base_url = https://esploradati.istat.it/SDMXWS/rest`
- `client.data_base_url = https://esploradati.istat.it/SDMXWS/rest`

## Rischi residui

- alcuni filtri multi-valore sul flow restituiscono `404`; il pilot evita per ora query piu larghe
- resta da capire se il flow supporta bene il fetch regionale in modo stabile dal plugin
