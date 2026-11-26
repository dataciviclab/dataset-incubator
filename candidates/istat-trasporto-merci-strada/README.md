# istat-trasporto-merci-strada

**Trasporto merci su strada — ISTAT `121_330` via DBnomics (2008-2024)**

## Domanda civica

Quanta merce muove ogni regione su strada, in **entrata** e in **uscita**? Il trasporto su strada è la modalità dominante, ma il dibattito resta spesso nazionale: l'origine-destinazione regionale mostra quali territori spediscono merci e quali le ricevono.

## Dataset

- **Fonte**: ISTAT `121_330`, canale **DBnomics** (`type: dbnomics`, provider ISTAT) — mirror, nessun rate-limit SDMX.
- **Copertura**: 2008-2024; `years: [2026]` è l'anno di output.
- **Dimensioni**: `REG_LOADING` (regione di carico), `REG_UNLOADING` (regione di scarico), `GOODS_TRANSPORT_NST_2007`, `TITLE_OF_TRANSPORT`, `DATA_TYPE`, `DISTANCE_CLASS`.
- **Misura**: `OBS_VALUE` (tonnellate-km, `GC_TKM`).

## Perché vale la pena

- Espone l'**origine-destinazione regionale**, che Eurostat non pubblica.
- Permette di leggere saldi regionali (più uscita o più entrata) e la quota di merci movimentate.
- È confrontabile con `istat-trasporto-ferroviario` (stessa unità `GC_TKM`).

## Output minimo atteso

- Clean: `anno`, `regione_carico`, `regione_scarico`, `merce_nst`, `tipo_trasporto`, `unita`, `classe_distanza`, `valore`.
- `mart_merci_per_direttrice`: per anno e regione, `tkm_uscita`, `tkm_entrata`, `tkm_movimentati`, `saldo_uscita_entrata`, `quota_pct` (quota sul totale dei flussi regionali, esclusi `IT -> IT`).

## Criterio di promozione

- Serie 2008-2024 leggibile per regione.
- Confronto documentato con il ferroviario e con Eurostat.

## Stato

`candidate` — run verificato e pubblicato.

## Prossimo passo

- Valutare un dettaglio per merceologia o classe di distanza, se la serie lo sostiene.
