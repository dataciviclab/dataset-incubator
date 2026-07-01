## Tecnico

- File unico CSV multi-anno (2018-2024)
- Encoding: UTF-8, delim: virgola
- Decimale: punto (es. 22.77)
- 47.419 righe, 29 colonne
- Granularità: singolo centro per data di rilevazione

## Analitico

- I centri CAS (Accoglienza Straordinaria) sono la tipologia dominante
- CPA (Centri di Prima Accoglienza) e Hotspot sono molto meno numerosi
- `costo_giornaliero_per_ospite` varia da ~22€ a ~45€
- `presenze_giornaliere` ha valori NULL in alcuni record (da verificare)
- Alcuni CPA mostrano tasso occupazione >100% (sovraffollamento)
- La geografia include codici ISTAT a tutti i livelli (comune, provincia, regione)

## Cautele

- La serie storica è omogenea su tutti gli anni? Sì, 2018-2024 continui
- Discontinuità: SAI/SIPROIMI non sono in questo CSV (file separato)
- Il file bandi ANAC non è accessibile (Access Denied)
- `tipologia_centro` ha varianti testuali da normalizzare (es. "CAS ADULTI", "CAS ADULTI UOMINI")
- `presenze_giornaliere` ha valori NULL possibili
