# gse-cer-elenco

**Elenco Nazionale Comunità Energetiche Rinnovabili (2025)** — GSE, Gestore dei Servizi Energetici.

Fonte: https://www.gse.it/servizi-per-te_site/autoconsumo_site/Documents/Elenco%20Comunit%C3%A0%20Energetiche%20Rinnovabili.xlsx
Issue intake: #720

## Domanda

Dove nascono le Comunità Energetiche Rinnovabili in Italia? Quante CER sono attive, con che potenza, e in quali territori?

## Dataset

- **Copertura**: nazionale — 20 regioni, 904 CER accreditate
- **Snapshot**: 31/12/2025
- **Colonne**: denominazione, potenza_kw, n_impianti, n_utenze, comune, provincia, regione, latitudine, longitudine, area_convenzionale, distributore, data_aggiornamento
- **Volumi**: 94,96 MW totali, 8.653 utenze, 1.429 impianti
- **Mart**: `mart_cer_riepilogo` con riepilogo per regione

## Perché vale la pena

- Tema caldo: le CER sono pilastro della transizione energetica e del PNRR
- Complementare ai dataset Terna esistenti (capacità rinnovabile, mix elettrico)
- Granularità_FINE: coordinate geografiche, comune, cabina primaria
- Unicità: unico dataset nazionale che elenca tutte le CER accreditate

## Output minimo atteso

Clean parquet + mart regionale. Top regioni per n_cer: Lombardia, Piemonte, Sicilia, Veneto.

## Stato

- [x] scaffold + run raw/clean/mart
- [ ] PR + review
