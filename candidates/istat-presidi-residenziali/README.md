# ISTAT — Presidi residenziali socio-assistenziali e socio-sanitari

Offerta di strutture residenziali per anziani e altri utenti (RSA, case di riposo,
comunità): numero di presidi, posti letto, personale e ospiti, per regione.

Il candidate usa `2023` come anno di run: il raw scarica l'intera serie e il
clean conserva **2009–2023**, così i mart producono la serie completa con un
solo fetch.

## Domanda civica

L'offerta di posti letto residenziali per anziani non autosufficienti è distribuita
in modo diseguale tra le regioni italiane, e con quale intensità di assistenza
sanitaria? Il divario Nord-Sud resta o si sta riducendo?

## Fonte

- **Ente**: ISTAT — indagine "Le strutture residenziali socio-assistenziali e
  socio-sanitarie"
- **Dataflow**: `49_37` (presidi, posti letto, personale) — DSD `DCIS_PRESIDI1`
- **Endpoint**: `https://esploradati.istat.it/SDMXWS/rest`
- **Formato**: SDMX (CSV/JSON)
- **Granularità**: regionale — Italia + 5 ripartizioni + 20 regioni/province autonome
- **Copertura**: 2009–2023

## Perché vale la pena

- Unica fonte nazionale che misura **offerta residenziale** (non ospedaliera):
  il Lab ha posti letto ospedalieri, non posti letto residenziali/LTC.
- Permette di isolare il perimetro **RSA**: utenza `ELD` (anziani) × livello di
  assistenza sanitaria (`MED`/`HIGH`).
- Include già i tassi per 100.000 residenti calcolati da ISTAT (`DATA_TYPE` 72/75),
  senza join a popolazione.

## Output minimo atteso

- `mart_sintesi_regione`: una riga per area e anno — n. presidi, posti letto,
  posti letto per 100k, posti letto anziani, quota anziani, personale.
- `mart_posti_letto_regione`: posti letto per area × tipo utenza × livello di
  assistenza sanitaria.
- `mart_trend`: primo/ultimo anno, delta e CAGR dei posti letto per 100k per area.

## Criterio di promozione

Serie 2009–2023 completa, mart `sintesi` + `trend` per regione, e una pagina
Explorer che mostri il divario Nord-Sud e l'intensità assistenziale.

## Stato / prossimo passo

- Candidate completo: run 2023, readiness **8/8 ready**.
- Serie 2009–2023 nei mart (clean 29.694 righe, mart 5.720 righe).
- Prossimo passo: PR e, se serve, secondo candidate sugli **ospiti** (`49_62`).
