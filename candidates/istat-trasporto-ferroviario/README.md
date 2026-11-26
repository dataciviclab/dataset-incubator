# istat-trasporto-ferroviario

**Trasporto ferroviario merci — ISTAT `117_1057` via DBnomics (2004-2024)**

## Domanda civica

Quanta merce viaggia su rotaia e quanta parte è **intermodale** (container, semi-rimorchi, casse mobili)? Il trasporto ferroviario è la leva principale per spostare merci dalla strada, ma senza il dettaglio per unità di carico e per origine/destinazione il confronto resta nazionale e indistinto.

## Dataset

- **Fonte**: ISTAT `117_1057`, canale **DBnomics** (`type: dbnomics`, provider ISTAT) — mirror, nessun rate-limit SDMX.
- **Copertura**: 2004-2024; `years: [2026]` è l'anno di output.
- **Dimensioni**: `REF_AREA`, `DATA_TYPE` (unità), `GOODS_TRANSPORT_NST_2007`, `INTERMODAL_TR_UNIT` (unità di carico), `COUNTRY_GOOD_ORIGIN` / `COUNTRY_GOOD_DESTINATION`, `CATEG_TRANSPORT`.
- **Misura**: `OBS_VALUE` (tonnellate-km, `GC_TKM`).

## Perché vale la pena

- Espone l'**unità di carico** e l'**origine-destinazione per paese**, due grandezze che Eurostat non pubblica a questo dettaglio.
- Permette di separare la crescita del trasporto ferroviario da quella della sua quota intermodale.
- È la base per un confronto rotaia/strada con `istat-trasporto-merci-strada` (stessa unità `GC_TKM`).

## Output minimo atteso

- Clean: `anno`, `area`, `unita`, `merce_nst`, `unita_carico`, `paese_origine`, `paese_destinazione`, `categoria_trasporto`, `valore`.
- `mart_ferrovia_intermodale`: per anno, `tkm_intermodale` (`TOT_INTERMODAL`), `tkm_totali` (`ALL`) e `quota_intermodale_pct`.

## Criterio di promozione

- Quota intermodale leggibile su 2009-2024 (2004-2008 senza `TOT_INTERMODAL`, quota `NULL`).
- Confronto documentato con `istat-trasporto-merci-strada` e con Eurostat.

## Stato

`candidate` — run verificato e pubblicato.

## Prossimo passo

- Verificare la copertura di `REF_AREA` e delle dimensioni costanti (`ALL`/`WORLD`).
- Eventuale mart origine-destinazione per paese se la serie lo sostiene.
