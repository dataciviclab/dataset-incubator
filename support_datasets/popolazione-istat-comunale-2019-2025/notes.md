# Notes — popolazione-istat-comunale-2019-2025

## Support dataset

Base infrastrutturale per join e coverage check. Non è un filone narrativo autonomo.

## Fonte

- ISTAT POSAS `POSAS_{year}_it_Comuni.zip`
- URL: `https://demo.istat.it/data/posas/POSAS_{year}_it_Comuni.zip`
- Formato: ZIP → CSV, `;` delim, `utf-8` con BOM, skip 1 riga
- Chiave: `codice_comune`

## Run completati (2026-04-27)

Tutti e 7 gli anni: raw ✅ clean ✅ mart ✅

2020-2023 erano PENDING (clean/mart non partiti per timeout). Rilanciati oggi — nessun problema di schema.

## Schema

- Clean: 20 colonne, raw-faithful
- `popolazione_by_comune`: 1 riga per comune (ETA=999 totale)
- `popolazione_by_eta`: 1 riga per comune per classe di età (ETA 0-100)

## Cautele

- `comune` è descrittivo — usare `codice_comune` come chiave
- Variazioni territoriali / fusioni di comuni nel periodo possono creare mismatches nei join
- Non assumere schema perfettamente stabile senza verifica su ogni anno

## IRPEF join test

Con IRPEF 2023: ~7892 match su ~7897 comuni (99,9%). I pochi non-match confermano il dataset come detector di anomalie territoriali.


