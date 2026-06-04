# Note — strutture-asl

## Rischi noti
- Nomi colonna nel CSV con spazi finali (`"Regione "`) — il clean.sql fa TRIM
- Encoding latin-1, delimiter `;`
- `Codice Regione` come VARCHAR (es. `"010"`) — ok per join
- File aggiornato a maggio 2024 — potrebbe non essere l'ultimo disponibile
