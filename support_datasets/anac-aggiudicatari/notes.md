# Note tecniche — anac-aggiudicatari (support)

## Struttura fonte

CKAN dataset `aggiudicatari` su dati.gov.it (harvesting ANAC):
- Full dump: risorsa `aggiudicatari_csv` (~800MB ZIP, ~5.4M righe)
- Delta mensili: risorse `YYYYMMDD-aggiudicatari_csv` (non inclusi)
- Senza DataStore — download diretto CSV via filesystem API

Config: `resource_name: "aggiudicatari_csv"` + extractor `unzip_first_csv`.
Stessa identica strategia di `anac-aggiudicazioni`.

## Schema osservato

Da delta JSON `20260701-aggiudicatari_json.json` (2.242 righe):
- `cig` — VARCHAR, CIG
- `ruolo` — VARCHAR (OPERATORE ECONOMICO MONOSOGGETTIVO, IMPRESA AUSILIARIA, ecc.)
- `codice_fiscale` — VARCHAR (può essere null per operatori esteri)
- `denominazione` — VARCHAR (ragione sociale, a volte con spazi extra)
- `tipo_soggetto` — VARCHAR (IMPRESA, DITTA INDIVIDUALE, NON PRESENTE IN ANAGRAFE, ecc.)
- `id_aggiudicazione` — BIGINT (negativo = senza corrispondenza in anagrafica)

## Join chain

```
anac_bandi_gara (cig) → anac_aggiudicazioni (cig)
anac_aggiudicazioni (id_aggiudicazione) → anac_aggiudicatari (id_aggiudicazione)
```

## Qualità dati (run 2026-07-18)

| Metrica | Valore |
|---|---|
| Righe totali | 5.437.334 |
| Join con anac_aggiudicazioni via id_aggiudicazione | 9.424.624 match |
| Operatori economici distinti (denominazione) | ~505K |

**Anomalie note (non bloccanti):**
- `codice_fiscale` nullo per operatori non censiti in anagrafe o esteri
- `id_aggiudicazione` negativo (-1, -2xxxx) indica assenza di corrispondenza anagrafica
- `denominazione` con spazi extra o case incoerente (es. "IMPRESA INESISTENTE")
