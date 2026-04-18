# ISTAT - Delitti Denunciati (2010-2015)

Dataset estratto dal mirror pubblico DBnomics del dataset ISTAT sui delitti denunciati dalle Forze di Polizia all'Autorità Giudiziaria.

La fonte primaria desiderata resta ISTAT SDMX. In questa versione il candidate usa DBnomics come mirror operativo perché l'endpoint SDMX diretto e' risultato instabile durante il run; la scelta e' documentata in `notes.md`.

## Struttura Dati
- `codice_territorio`: Codice ISTAT dell'area geografica.
- `territorio`: Denominazione ISTAT dell'area geografica.
- `codice_reato`: Codice ISTAT della tipologia di delitto (es. THEFT, RAPE, INTENHOM).
- `reato`: Denominazione della tipologia di delitto.
- `anno`: Anno di riferimento.
- `numero_denunce`: Conteggio totale delle denunce.

## Note Tecniche
I dati sono acquisiti dal provider DBnomics `ISTAT/73_67_DF_DCCV_DELITTIPS_1` in CSV. Il layer clean filtra l'indicatore `CRIMEN`, territorio Italia, autore totale e delitti durante l'anno di riferimento.

La partizione runtime e' `2015`; il mart contiene la serie storica 2010-2015 per l'Italia.
