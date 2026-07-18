# Note tecniche — anac-partecipanti (support)

## Struttura fonte

CKAN dataset `partecipanti` su dati.gov.it (harvesting ANAC):
- Full dump: risorsa `partecipanti_csv` (~1GB ZIP)
- Delta mensili: risorse `YYYYMMDD-partecipanti_csv` (non inclusi)
- Stesso pattern di `anac_aggiudicatari`: 5 colonne, delim `;`

Config: `resource_name: "partecipanti_csv"` + extractor `unzip_first_csv`.

## Schema (5 colonne)

| Colonna | Tipo | Descrizione |
|---|---|---|
| `cig` | VARCHAR | CIG della gara |
| `ruolo` | VARCHAR | Ruolo del partecipante |
| `codice_fiscale` | VARCHAR | CF/P.IVA del partecipante |
| `denominazione` | VARCHAR | Ragione sociale |
| `tipo_soggetto` | VARCHAR | Tipo soggetto |

## Differenza con anac_aggiudicatari

`anac_aggiudicatari` contiene solo gli **operatori che hanno vinto** la gara.
`anac_partecipanti` contiene **tutti i partecipanti**, vincitori e non.

Join via `codice_fiscale` per incrociare chi partecipa e chi vince.

## Qualità dati (run 2026-07-18)

| Metrica | Valore |
|---|---|
| Righe totali | 8.044.052 |
| CIG distinti | 4.746.047 |
| Partecipanti distinti (CF) | ~578K |
| CF nulli | 0 ✅ |
| CIG nulli | 0 ✅ |
| Righe per CIG (media) | 1,7 |
| Match con anac_aggiudicazioni | 7.673.210 (95%) |
| Match con anac_bandi_gara 2025 | 1.793.021 |

## Anomalie note

- `ruolo` spesso nullo (dal delta osservato, la colonna era vuota)
- Full dump non rigenerato frequentemente (2023 + delta cumulativi)
- 1,7 partecipanti/CIG di media — valori più alti possibile per gare con molte offerte
