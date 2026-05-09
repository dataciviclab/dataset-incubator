# Note: Giustizia penale - clearance rate e disposition time

## Rischi noti

- Il dataset è di **indicatori già derivati** — clearance rate e disposition time sono calcolati, non flussi grezzi. Non permette di ricostruire i procedimenti originali.
- Il margine di costruzione analitica è ridotto rispetto ai dataset di flusso.
- L'unità di analisi più interessante è distretto × anno, non singola sede.

## Decisioni prese

- Partiamo dal sheet **Tribunali** (il più ricco, 4621 righe). Gli altri sheet (Corti d'Appello, Giudici di Pace, Tribunale per i Minorenni) hanno struttura simile e possono essere aggiunti in un secondo momento.
- Anni: 2014-2023 (10 anni pieni disponibili).

## Cosa monitorare dopo il run

- Schema colonne: tolerance su "Anno" integer e "Clearance rate" / "Disposition time" double
- Null rate su clearance_rate e disposition_time — indicatori calcolati, potrebbero avere NaN dove il denominatore è zero
- Range valori: clearance rate dovrebbe essere intorno a 0.5-2.0, disposition time in giorni (200-700 gg circa)