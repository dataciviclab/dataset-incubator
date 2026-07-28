# Note tecniche — siope-bilancio-unificato

## Fonte

Clean parquet generati da [open-siope](https://github.com/dataciviclab/open-siope),
pubblicati su GCS pubblico:
- `https://storage.googleapis.com/dataciviclab-clean/siope/siope_entrate/{year}/siope_entrate_{year}_clean.parquet`
- `https://storage.googleapis.com/dataciviclab-clean/siope/siope_uscite/{year}/siope_uscite_{year}_clean.parquet`

Il dato upstream proviene dai download open di [SIOPE](https://www.siope.it).

## Perimetro

- 2021-2026
- Entrate + uscite di tutti i comparti SIOPE
- ~18.000 enti, ~13M righe/anno
- Granularità mensile (periodo 01..12)

## Join e arricchimento

Tutti i join (territorio, comparto, classificazione voci) sono già stati
eseguiti a monte in open-siope. Il dato downstream è già arricchito.
La colonna `lato` viene aggiunta all'ingresso tramite inject_column.

## Output

Il layer **clean** contiene il bilancio unificato completo (entrate+uscite,
stessa granularità del dato upstream).

I **mart** analitici sono tre:
- `mart_sintesi`: entrate/uscite per comparto × regione × anno
- `mart_trend`: CAGR entrate/uscite per comparto × regione
- `mart_enti`: benchmark entrate/uscite per singolo ente

Non esiste più un mart passthrough (`siope_bilancio_unificato`): per il dato
full si usa il clean (via clean-query MCP o direttamente da GCS).

## Rischi

- Il path GCS dei clean (`dataciviclab-clean/siope/siope_entrate/` e
  `siope_uscite/`) è un contratto con open-siope. Se cambia, il candidate
  si rompe.
- I dati SIOPE vengono aggiornati mensilmente dalla fonte. Il candidate va
  rieseguito periodicamente per avere i dati freschi.
- Le colonne divergenti tra entrate e uscite (`macro_categoria_v2` vs
  `macro_area`/`macro_categoria`) vengono allineate automaticamente da
  read_parquet(union_by_name=true).
