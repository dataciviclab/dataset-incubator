# Note: Giustizia penale - clearance rate e disposition time

## Rischi noti

- Il dataset è di **indicatori già derivati** — clearance rate e disposition time sono calcolati, non flussi grezzi. Non permette di ricostruire i procedimenti originali.
- Il margine di costruzione analitica è ridotto rispetto ai dataset di flusso.
- L'unità di analisi più interessante è distretto × anno, non singola sede.

## Update (issue #693)

- **Prima**: solo sheet Tribunali, 4.620 righe, 2014-2024
- **Dopo**: 4 sheet unificati, ~12.700 righe, 2014-2025
- Il file XLSX è `Indicatori_Penali.xlsx` (non più `Indicatori_Penali_1.xlsx`)
- Script `scripts/unite_sheets_penali.py` per unire i 4 sheet in CSV

## Cosa monitorare dopo il run

- Schema colonne: tolerance su "Anno" integer e "Clearance rate" / "Disposition time" double
- Null rate su clearance_rate e disposition_time — indicatori calcolati, potrebbero avere NaN dove il denominatore è zero
- Range valori: clearance rate dovrebbe essere intorno a 0.5-2.0, disposition time in giorni (200-700 gg circa)
- Verificare che tutti i 4 sheet siano rappresentati nel dato finale

## Da fare
- [ ] Verificare che lo script unite_sheets funzioni con il file reale
- [ ] Validare che Tribunali pre/post update diano gli stessi valori (backward compat)
