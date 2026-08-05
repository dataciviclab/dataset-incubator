# camera-gruppi

**Domanda guida:** Quali gruppi parlamentari sono esistiti alla Camera, con quale denominazione e in quale legislatura? A quale nome corrisponde l'URI `gr1612` che compare in `camera_incarichi`?

**Fonte:** Camera dei Deputati — OpenData SPARQL (`https://dati.camera.it/sparql`)
**Dataset:** classe `ocd:gruppoParlamentare` (239 gruppi, tutte le legislature)
**Licenza:** CC BY 3.0

## Perché vale la pena

`camera_incarichi` espone gli incarichi con il solo URI del gruppo (`gr1612`): senza anagrafica non si sa *quale* gruppo sia (M5S? FI? PD?). Questo support dataset dà il nome (label completa con acronimo e date) e la legislatura. Join con `camera_incarichi` via URI gruppo.

## Output minimo atteso

- `camera_gruppi`: gruppo (URI), nome (label), legislatura — 239 righe
- `mart_gruppi_legislatura`: gruppi per legislatura

## Criterio di promozione

Promuovere quando il join con `camera_incarichi` (via URI gruppo) è verificato e almeno una domanda usa i nomi dei gruppi (es. "quale gruppo ha più turnover di ruoli?").

## Stato / prossimo passo

- **Stato**: support a standard v1 (2026-08-04) — run ok, join con camera_incarichi verificato 100%
- **Prossimo passo**: promozione
