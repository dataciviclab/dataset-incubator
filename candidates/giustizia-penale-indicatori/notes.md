# Note: Giustizia penale - clearance rate e disposition time

## Rischi noti

- Il dataset è di **indicatori già derivati** — clearance rate e disposition time sono calcolati, non flussi grezzi. Non permette di ricostruire i procedimenti originali.
- Il margine di costruzione analitica è ridotto rispetto ai dataset di flusso.
- L'unità di analisi più interessante è distretto × anno, non singola sede.

## Update (issue #693)

- **Prima**: solo sheet Tribunali, 4.620 righe, 2014-2024, file `Indicatori_Penali_1.xlsx`
- **Dopo**: 4 sheet unificati, **10.478 righe**, 2014-2025, file `Indicatori_Penali.xlsx`
- Script: `scripts/unite_sheets_penali.py` — scarica il XLSX via `lab_connectors.http.download` e unisce i 4 sheet in CSV
- Il run richiede `TOOLKIT_ALLOW_SCRIPT_SOURCE=1` (script source abilitato)

## Cosa monitorare dopo il run

- Schema colonne: tolerance su "Anno" integer e "Clearance rate" / "Disposition time" double
- Null rate su clearance_rate e disposition_time — il clean.sql filtra i NULL, quindi righe con indicatori mancanti vengono scartate
- Range valori: clearance rate intorno a 0.5-2.0, disposition time in giorni (200-700 gg circa)
- Confronto backward compat: i valori Tribunali pre/post update sono identici (stessa fonte, stesso sheet)

## Da fare

- [x] Script unite_sheets_penali.py funzionante con download autonomo
- [x] Validazione 4 sheet unificati (10.478 righe)
- [ ] Notebook `giustizia_penale_indicatori_v0.ipynb` con analisi esplorativa
- [ ] Promozione da incubating a published in clean_catalog.json
