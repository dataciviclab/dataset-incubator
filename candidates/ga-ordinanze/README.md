# ga-ordinanze — Ordinanze Giustizia Amministrativa (OpenGA)

Dataset unificato delle ordinanze del Consiglio di Stato e dei Tribunali Amministrativi Regionali, proveniente dal portale [OpenGA](https://openga.giustizia-amministrativa.it).

## Copertura

- **31 sedi**: CdS, CGA Sicilia, 27 TAR, 2 TRGA
- **4 anni**: 2023–2026 (aggiornamento MONTHLY)

## Schema

Stesso schema identico di `ga-sentenze` (17 colonne). Chiave `NUMERO_RICORSO` per join.

## Mart

| Tabella | Descrizione |
|---|---|
| mart_esiti_per_sede | Esiti per sede/anno |
| mart_esiti_per_tipo | Esiti per tipo ricorso/anno |
