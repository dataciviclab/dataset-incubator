# ISTAT - Delitti Denunciati (2010-2015)

Dataset estratto dai flussi SDMX ISTAT relativi ai delitti denunciati dalle Forze di Polizia all'Autorità Giudiziaria.

## Struttura Dati
- `codice_territorio`: Codice ISTAT dell'area geografica.
- `codice_reato`: Acronimo del reato (es. THEFT, ARSON, CYBERCRIM).
- `anno`: Anno di riferimento.
- `numero_denunce`: Conteggio totale delle denunce.

## Note Tecniche
I dati sono stati estratti processando i tag `<generic:Series>` e `<generic:Obs>` dai file XML originali, gestendo le sequenze di escape dei caratteri speciali.