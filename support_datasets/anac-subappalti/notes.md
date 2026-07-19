# Note tecniche — anac-subappalti (support)

## Struttura fonte

CKAN dataset `subappalti` su dati.gov.it (harvesting ANAC):
- Full dump: risorsa `subappalti_csv` (~122MB ZIP)
- Delta: risorse YYYYMMDD-subappalti_csv (6-15MB)
- Frequenza: ANNUALE
- Stessa identica configurazione di `anac_partecipanti`

## Qualità dati (run 2026-07-19)

| Metrica | Valore |
|---|---|
| Righe | 334.301 |
| Con cf_subappaltante | dati da verificare |
| CIG nulli | 0 ✅ |
| Match con anac_aggiudicazioni | da verificare |

## Note

- `classe_importo` è VARCHAR nel CSV (es. "null" o valori testuali)
- `cf_subappaltante` può essere nullo (subappalti dove non è stato indicato l'affidatario principale)
- I CIG qui sono CIG ordinari (numerici), joinabili con bandi/aggiudicazioni
