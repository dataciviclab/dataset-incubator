# Note — strutture-ricovero-asl

## Rischi noti
- Colonna `Regione` con R maiuscola (diverso da altri CSV) — il clean.sql usa `"Regione"`
- `ricoveri` e `giornate_degenza` come DOUBLE (non VARCHAR con separatore) — attenzione se si cambia fonte
- File aggiornato a gennaio 2025 (dicitura nel filename)
- Molise e Valle d'Aosta mostrano valori anomali su `personale_osp_per_100k` nel compose (segnalato in PR #15)
